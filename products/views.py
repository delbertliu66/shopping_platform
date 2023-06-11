import json

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from .models import Categories,Products
from rest_framework import status
from .serializers import ProductSerializers, CategorySerializers


cate_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/catalog/categories'
prod_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/catalog/products'

headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


class ProductsView(APIView):

    # 获取所有产品列表
    def get(self, request):
        products = cache.get('products')
        if products is not None:
            return Response({
                'code': 200,
                'msg': 'success',
                'data': {
                    'products': products
                }
            })

        result = requests.get(url=prod_url, headers=headers)
        if result.status_code == 200:
            cache.set('products', result.json()['data'])
            return Response({
                'code': 200,
                'msg': 'success',
                'data': {
                    'products': result.json()['data']
                }
            })
        else:
            return Response(result.json(), status=result.status_code)

    # 新增一个产品
    def post(self, request):
        prod_data = request.data.copy()

        # 先将产品分类查出来
        category = get_object_or_404(Categories, bc_cate_id=request.data['categories'][0])
        prod_data.pop('categories', None)

        # 先在bc店铺中新建产品并保存
        result = requests.post(url=prod_url, headers=headers, data=json.dumps(request.data))

        if result.status_code == 200:
            Products.objects.create(
                **prod_data,
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
        prod_data = request.data.copy()
        prod_id = request.data['id']
        # 先查询是否有要修改的记录
        product = Products.objects.filter(bc_pro_id=prod_id).first()

        if not product:
            return Response({
                'code': 400,
                'msg': 'Product does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先更新bc店铺
        url = prod_url + "/" + str(prod_id)
        prod_data.pop('id', None)
        result = requests.put(url=url, headers=headers, data=json.dumps(prod_data))

        if result.status_code == 200:
            if 'categories' in prod_data:
                category = Categories.objects.get(bc_cate_id=prod_data['categories'][0])
                product.category = category
                prod_data.pop('categories', None)

            for key, value in prod_data.items():
                if hasattr(product, key):
                    setattr(product, key, value)
            product.save()

            return Response(result.json(), status=result.status_code)

        else:
            return Response(result.json(), status=result.status_code)

    # 删除产品
    def delete(self, request):
        prod_ids = request.data['ids']
        product = Products.objects.filter(bc_pro_id__in=prod_ids)

        if not product.exists():
            return Response({
                'code': 400,
                'msg': 'Invalid ids'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先删除bc店铺数据
        url = prod_url + '?' + 'id:in={}'.format(','.join(str(_id) for _id in prod_ids))
        result = requests.delete(url=url, headers=headers)

        if result.status_code == 204:
            product.delete()
            return Response({
                'code': 204,
                'msg': 'delete successful'
            }, status=result.status_code)
        else:
            return Response(result.json())


class CategoriesView(APIView):

    # 获取所有商品分类
    def get(self, request):
        categories = cache.get('categories')
        if categories is not None:
            return Response({
                'code': 200,
                'msg': 'success',
                'data': {
                    'categories': categories
                }
            })

        result = requests.get(cate_url, headers=headers)
        if result.status_code == 200:
            cache.set('categories', result.json().get('data'))
            return Response({
                'code': 200,
                'msg': 'success',
                'data': {
                    'categories': result.json().get('data')
                }
            })
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
                bc_cate_id=result.json()['data']['id'],
                **cate_data
            )
            return Response(result.json(), status=result.status_code)
        else:
            return Response(result.json(), status=result.status_code)

    # 更新商品分类
    def put(self, request):
        cate_data = request.data.copy()
        cate_id = request.data['id']

        # 先查询输入的id是否存在对应的记录
        category = get_object_or_404(Categories, bc_cate_id=cate_id)
        # 如果存在记录，判断修改的名字是否重复，判断修改的parent_id是否存在
        if 'name' in cate_data:
            category_exists = Categories.objects.filter(name=cate_data['name']).exists()
            if category_exists:
                return Response({
                    'code': 400,
                    'msg': 'New category name already exists!'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                category.name = cate_data['name']
        if 'parent_id' in cate_data:
            category_exists = Categories.objects.filter(bc_cate_id=cate_data['parent_id']).exists()
            if not category_exists and cate_data['parent_id'] != 0:
                return Response({
                    'code': 400,
                    'msg': 'parent_id does not exist!'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                category.parent_id = cate_data['parent_id']

        cate_data.pop('id', None)
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
        cate_ids = request.data['ids']
        # 判断要删除的记录是否存在
        category = Categories.objects.filter(bc_cate_id__in=cate_ids)

        if not category.exists():
            return Response({
                'code': 400,
                'msg': 'Enter error id'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 先删除bc店铺的数据
        url = cate_url + '?' + 'id:in={}'.format(','.join(str(_cate_id) for _cate_id in cate_ids))
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


class ProductDetailsView(APIView):

    # 获取单个产品详情
    def get(self, request):
        prod_id = request.GET.get('id')
        product = cache.get(f'product:{prod_id}')
        if product:
            product_data = ProductSerializers(product).data
            return Response({
                'code': 200,
                'msg': 'success',
                'data': product_data
            })

        product = Products.objects.filter(bc_pro_id=prod_id).first()
        if product:
            product_data = ProductSerializers(product).data
            cache.set(f'product:{product.bc_pro_id}', product, timeout=60 * 10)
            return Response({
                'code': 200,
                'msg': 'success',
                'data': product_data
            })
        else:
            return Response({
                'code': 400,
                'msg': 'Invalid id!'
            }, status=status.HTTP_400_BAD_REQUEST)
