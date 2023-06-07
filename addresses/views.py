import json

from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests

from addresses.models import Addresses
from customers.models import Customers

headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

address_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses'


# Create your views here.
class AddressesView(APIView):

    # 获取customer的地址
    # http://127.0.0.1:8000/shop/api/v1/customers/addresses
    def get(self, request):
        result = requests.get(url=address_url, headers=headers)

        if result.status_code == 200:
            return Response(result.json())
        else:
            return Response(result.json(), status=result.status_code)

    # 新增customer的地址
    def post(self, request):
        address_data = request.data.copy()
        # 从请求体中获取customer_id
        customer_id = request.data['customer_id']
        # 根据customer_id查询是否存在该用户
        customer = get_object_or_404(Customers, bc_id=customer_id)
        # 输入的customer_id存在用户，则添加，先在bc店铺添加，再本地数据库添加
        result = requests.post(url=address_url, headers=headers, data=json.dumps([request.data]))

        if result.status_code == 200:
            # bc店铺添加成功
            # 筛选字典解构数据
            address_data.pop('customer_id', None)
            new_address = Addresses.objects.create(
                address_id=result.json()['data'][0]['id'],
                # 字典解构，将字典中的key和value逐一赋值给address中的属性和值(不能含有对象没有的属性只，否则报错)
                **address_data,
                customer=customer
            )
            return Response(result.json())
        else:
            return Response(result.json(), status=status.HTTP_404_NOT_FOUND)

    # 更新地址
    def put(self, request):
        address_data = request.data.copy()

        address = Addresses.objects.get(address_id=address_data['id'])

        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses'
        result = requests.put(url, headers=headers, data=json.dumps([request.data]))

        address_data.pop('id', None)
        if result.status_code == 200:
            # 优化代码
            for key, value in address_data.items():
                if hasattr(address, key):
                    setattr(address, key, value)
            address.save()
            return Response({
                'code': 200,
                'msg': 'update successful',
                'data': result.json()['data'][0]})
        else:
            return Response(result.json(), status=status.HTTP_404_NOT_FOUND)

    # 删除地址
    def delete(self, request):
        # 从查询参数中获取ids
        address_ids = request.data['ids']

        # 判断传入的address_id是否存在对应的记录
        address = Addresses.objects.filter(address_id__in=address_ids)
        if address.exists():
            url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses?id:in={}'.format(','.join(
                str(_id) for _id in address_ids))
            result = requests.delete(url, headers=headers)

            if result.status_code == 204:
                address.delete()
                return Response({
                    'code': 200,
                    'msg': 'delete successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response(result.json(), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'code': 404,
                'msg': "address_id invalid"
            }, status=status.HTTP_400_BAD_REQUEST)
