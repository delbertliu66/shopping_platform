import json

from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from customers.models import Customers
from addresses.models import Addresses
from .models import Orders,OrderItems
from products.models import Products
from rest_framework import status

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
        customer = get_object_or_404(Customers, bc_id=order_data['customer_id'])
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

                add_headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFsYmVydGxpdUAxNjMuY29tIiwiZXhwIjoxNjg2NTM4NzU2fQ.ciUJWAKkCrHatZaaOX_dczWDLzrqpm8aU2mzPA6qeX8'
                }

                add_address_result = requests.post(
                    url='http://127.0.0.1:8000/shop/api/v1/customers/addresses',
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

    # 更新订单信息
    def put(self, request):
        pass

    # 删除一条订单
    def delete(self, request):
        bc_order_id = request.query_params.get('id')

        order = Orders.objects.filter(bc_order_id=bc_order_id)
        if not order.exists():
            return Response({
                'code': 400,
                'msg': 'id does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

        # https://api.bigcommerce.com/stores/{store_hash}/v2/orders/{order_id}
        url = order_url + '/' + str(bc_order_id)

        result = requests.delete(url=url, headers=headers)

        if result.status_code == 204:
            order.delete()

            return Response({
                'code': 204,
                'msg': 'delete successful'
            }, status=result.status_code)
        else:
            return Response(result.json(), status=result.status_code)









