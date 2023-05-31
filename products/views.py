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
    pass


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
