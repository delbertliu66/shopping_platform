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


# Create your views here.
class AddressesView(APIView):

    # 获取customer的地址
    # http://127.0.0.1:8000/shop/api/v1/customers/addresses
    def get(self, request):
        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses'
        result = requests.get(url, headers=headers)

        if result.status_code == 200:
            return Response(result.json())
        else:
            return Response(result.json(), status=result.status_code)

    # 新增customer的地址
    # https://api.bigcommerce.com/stores/{store_hash}/v3/customers/addresses
    def post(self, request):
        address_data = request.data
        # 从请求体中获取customer_id
        customer_id = address_data['customer_id']
        # 根据customer_id查询是否存在该用户
        # customer = get_object_or_404(Customers, id=customer_id)
        customer = Customers.objects.get(bc_id=customer_id)
        # 如果输入的customer_id查询出啦没有用户
        if not customer:
            return Response({
                'code': 404,
                'msg': "customer_id invalid"
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            # 输入的customer_id存在用户，则添加，先在bc店铺添加，再本地数据库添加
            url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses'
            list_data = [address_data]
            # print(list_data)
            result = requests.post(url, headers=headers, data=json.dumps(list_data).encode('utf8'))

            if result.status_code == 200:
                # bc店铺添加成功
                new_address = Addresses.objects.create(
                    address_id=result.json()['data'][0]['id'],
                    address1=address_data['address1'],
                    address2=address_data['address2'],
                    address_type=address_data['address_type'],
                    city=address_data['city'],
                    company=address_data['company'],
                    country_code=address_data['country_code'],
                    first_name=address_data['first_name'],
                    last_name=address_data['last_name'],
                    phone=address_data['phone'],
                    postal_code=address_data['postal_code'],
                    state_or_province=address_data['state_or_province'],
                    customer=customer
                )

                return Response(result.json())
            else:
                return Response(result.json(), status=status.HTTP_404_NOT_FOUND)

    # 更新地址
    def put(self, request):
        address_data = request.data

        address = Addresses.objects.get(address_id=address_data['id'])

        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers/addresses'
        result = requests.put(url, headers=headers, data=json.dumps([request.data]))

        # 待优化
        if result.status_code == 200:
            if 'address1' in address_data:
                address.address1 = address_data['address1']
            if 'address2' in address_data:
                address.address2 = address_data['address2']
            if 'address_type' in address_data:
                address.address_type = address_data['address_type']
            if 'city' in address_data:
                address.city = address_data['city']
            if 'company' in address_data:
                address.company = address_data['company']
            if 'country_code' in address_data:
                address.country_code = address_data['country_code']
            if 'first_name' in address_data:
                address.first_name = address_data['first_name']
            if 'last_name' in address_data:
                address.last_name = address['last_name']
            if 'phone' in address_data:
                address.phone = address_data['phone']
            if 'postal_code' in address_data:
                address.postal_code = address_data['postal_code']
            if 'state_or_province' in address_data:
                address.state_or_province = address_data['state_or_province']
            address.save()
            return Response({
                'code': 200,
                'msg': 'update successful',
                'data': result.json()['data'][0]})
        else:
            return Response(result.json(), status=status.HTTP_404_NOT_FOUND)


