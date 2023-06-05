import json

from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from customers.models import Customers
from addresses.models import Addresses
from .models import Orders,OrderItems
from products.models import Products
from addresses.views import AddressesView
from rest_framework.test import APIRequestFactory


headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
order_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v2/orders'


class OrdersView(APIView):

    # 获取所有订单列表
    def get(self, request):
        result = requests.get(url=order_url, headers=headers)
        return Response({
            'code': 200,
            'orders': result.json()
        }, status=result.status_code)

    # 新增一个订单
    def post(self, request):
        order_data = request.data
        address_data = order_data['billing_address']
        # 先查询出输入的数据
        customer = Customers.objects.get(bc_id=order_data['customer_id'])
        address = Addresses.objects.filter(
            customer_id=order_data['customer_id'],
            first_name=address_data['first_name'],
            last_name=address_data['last_name'],
            city=address_data['city'],
            state_or_province=address_data['state'],
            country_code=address_data['country_iso2']
        ).first()

        # 先在bc店铺新增order
        result = requests.post(url=order_url, headers=headers, data=json.dumps(order_data))
        if result.status_code == 201:
            # 新增成功，在本地数据库新增order
            # 如果地址不存在，则将地址信息新增
            if not address:
                data = {
                    'customer_id': order_data['customer_id'],
                    "address1": address_data['street_1'],
                    "address2": "",
                    "address_type": "residential",
                    "city": address_data['city'],
                    "company": "",
                    "country": address_data['country'],
                    "country_code": address_data['country_iso2'],
                    "first_name": address_data['first_name'],
                    "last_name": address_data['last_name'],
                    "phone": "",
                    "postal_code": str(address_data['zip']),
                    "state_or_province": address_data['state']
                }
                # 调用address中的post方法,新增地址
                # post_address_data = AddressesView.post(json.dumps(data))
                # response_content = post_address_data.content
                # address = Addresses.objects.get(address_id=response_content['id'])

                add_headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsYmVydGxpdUAxNjMuY29tIiwiZXhwIjoxNjg2NTM4NzU2fQ.ciUJWAKkCrHatZaaOX_dczWDLzrqpm8aU2mzPA6qeX8'
                }

                add_address_result = requests.post(
                    url='http://127.0.0.1:8000/shop/api/v1/customers/addresses/',
                    headers=add_headers,
                    data=json.dumps(data))
                address_id = add_address_result.content['data'][0].get('id')
                address = Addresses.objects.get(address_id=add_address_result)

            order = Orders.objects.create(
                customer=customer,
                bc_order_id=result.json()['id'],
                status=order_data['status_id'],
                address=address
            )

            # 新增订单item
            for product in order_data['products']:
                order_product = Products.objects.get(bc_pro_id=product['product_id'])
                order_item = OrderItems.objects.create(
                    order=order,
                    product=order_product,
                    quantity=product['quantity'],
                    total_price=int(product['quantity']) * order_product.price
                )

            # 订单item新增完成后，更新order中的总数量和总价
            order.update_quantity_price()
            return Response(result.json(), status=result.status_code)
        return Response(result.json(), status=result.status_code)






