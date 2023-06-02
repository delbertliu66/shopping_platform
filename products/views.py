import json

from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from .models import Categories,Products
from rest_framework import status


cate_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/catalog/categories'
prod_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/catalog/products'

headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


class ProductsView(APIView):

    # 获取所有产品列表
    # https://api.bigcommerce.com/stores/{store_hash}/v3/catalog/products
    def get(self, request):

        result = requests.get(url=prod_url, headers=headers)
        return Response(result.json(), status=result.status_code)

    # 新增一个产品
    def post(self, request):
        prod_data = request.data

        # 先将产品分类查出来
        category = Categories.objects.filter(name=prod_data['category']).first()
        # 如果输入的产品分类不存在
        if not category:
            return Response({
                'code': 400,
                'msg': 'Category not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先在bc店铺中新建产品并保存
        result = requests.post(url=prod_url, headers=headers, data=json.dumps(prod_data))

        if result.status_code == 200:
            Products.objects.create(
                name=prod_data['name'],
                type=prod_data['type'],
                weight=prod_data['weight'],
                price=prod_data['price'],
                sku=prod_data['sku'],
                bc_pro_id=result.json()['data']['id'],
                category=category
            )

            return Response({
                'code': 200,
                'msg': 'create product successful'
            })
        else:
            return Response(result.json(), status=result.status_code)

    # 更新产品信息
    def put(self, request):
        prod_data = request.data
        prod_id = request.query_params.get('id')
        # 先查询是否有要修改的记录
        product = Products.objects.get(bc_pro_id=prod_id)

        if not product:
            return Response({
                'code': 400,
                'msg': 'Product does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先更新bc店铺
        url = prod_url + "/" + str(prod_id)
        result = requests.put(url=url, headers=headers, data=json.dumps(prod_data))

        if result.status_code == 200:
            if 'name' in prod_data:
                product.name = prod_data['name']
            if 'type' in prod_data:
                product.type = prod_data['type']
            if 'weight' in prod_data:
                product.weight = prod_data['weight']
            if 'price' in prod_data:
                product.price = prod_data['price']
            if 'sku' in prod_data:
                product.sku = prod_data['sku']
            if 'category' in prod_data:
                category = Categories.objects.get(name=prod_data['category'])
                product.category = category
            product.save()

            return Response(result.json(), status=result.status_code)

        else:
            return Response(result.json(), status=result.status_code)


class CategoriesView(APIView):

    # 获取所有商品分类
    def get(self, request):
        result = requests.get(cate_url, headers=headers)
        return Response(result.json(), status=result.status_code)

    # 新增商品分类
    def post(self, request):
        cate_data = request.data
        # 先判断name是否重复
        new_category = Categories.objects.filter(name=cate_data['name'])
        # 如果存在同名，则不能添加
        if new_category.exists():
            return Response({
                'code': 400,
                'msg': 'Category name already exists!'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 如果不存在同名，则先在bc店铺新增
        result = requests.post(url=cate_url, headers=headers, data=json.dumps(cate_data))
        # 判断返回结果
        if result.status_code == 200:
            # 将数据存入本地数据库
            new_category = Categories.objects.create(
                name=cate_data['name'],
                bc_cate_id=result.json()['data']['id'],
                parent_id=cate_data['parent_id']
            )
            return Response(result.json(), status=result.status_code)
        else:
            return Response(result.json(), status=result.status_code)

    # 更新商品分类
    def put(self, request):
        cate_data = request.data
        cate_id = request.query_params.get('id')

        # 先查询输入的id是否存在对应的记录
        try:
            category = Categories.objects.get(bc_cate_id=cate_id)
        except Categories.DoesNotExist:
            # 如果不存在直接返回
            return Response({
                'code': 400,
                'msg': "Invalid id"
            }, status=status.HTTP_400_BAD_REQUEST)

        # 如果存在记录，判断修改的名字是否重复，判断修改的parent_id是否存在
        if 'name' in cate_data:
            new_category = Categories.objects.filter(name=cate_data['name'])
            if new_category.exists():
                return Response({
                    'code': 400,
                    'msg': 'New category name already exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                category.name = cate_data['name']
        if 'parent_id' in cate_data:
            new_category = Categories.objects.filter(bc_cate_id=cate_data['parent_id'])
            if not new_category.exists() and cate_data['parent_id'] != 0:
                return Response({
                    'code': 400,
                    'msg': 'parent_id does not exist!'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                category.parent_id = cate_data['parent_id']

        # 更新bc店铺数据
        url = cate_url + '/' + str(cate_id)
        result = requests.put(url=url, headers=headers, data=json.dumps(cate_data))

        if result.status_code == 200:
            category.save()
            return Response({
                'code': 200,
                'msg': 'update successful'
            })
        else:
            return Response(result.json(), status=result.status_code)

    # 删除商品分类
    def delete(self, request):
        cate_id = request.query_params.get('id')
        # 判断要删除的记录是否存在
        category = Categories.objects.filter(bc_cate_id=cate_id)

        if not category.exists():
            return Response({
                'code': 400,
                'msg': 'Enter error id'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先删除bc店铺的数据
        url = cate_url + '/' + str(cate_id)
        result = requests.delete(url=url, headers=headers)

        if result.status_code == 204:
            # 删除本地数据
            category.delete()
            return Response({
                'code': 204,
                'msg': 'delete successful'
            }, status=result.status_code)
        else:
            return Response(result.json(), status=result.status_code)
