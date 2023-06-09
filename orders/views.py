import json

from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from customers.models import Customers
from addresses.models import Addresses
from .models import Orders,OrderItems
from products.models import Products
from rest_framework import status
from .seriliazers import OrderSerializers, OrderItemSerializers

headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
order_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v2/orders'


class OrdersView(APIView):

    # 获取所有订单列表
    def get(self, request):
        orders = cache.get('orders')
        if orders:
            return Response({
                'code': 200,
                'orders': orders
            })

        result = requests.get(url=order_url, headers=headers)
        if result.status_code == 200:
            cache.set('orders', result.json(), timeout=60 * 10)
            return Response({
                'code': 200,
                'orders': result.json()
            })
        else:
            return Response(result.json(), status=result.status_code)

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
                    data=json.dumps(data)).json()
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

    # 删除一条订单
    def delete(self, request):
        bc_order_id = request.data['id']

        order = Orders.objects.filter(bc_order_id=bc_order_id)
        if not order.exists():
            return Response({
                'code': 400,
                'msg': 'id does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)

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


class OrderDetailsView(APIView):

    # 获取单个订单详情
    def get(self, request, order_id):
        order = cache.get(f'order:{order_id}')
        if order:
            order_data = OrderSerializers(order).data
            return Response({
                'code': 200,
                'msg': 'success',
                'data': order_data
            })
        order = Orders.objects.prefetch_related('items').filter(bc_order_id=order_id).first()
        if order:
            cache.set(f'order:{order.bc_order_id}', order)
            order_data = OrderSerializers(order).data
            return Response({
                'code': 200,
                'msg': 'success',
                'data': order_data
            })
        else:
            return Response({
                'code': 400
            }, status=status.HTTP_400_BAD_REQUEST)

    # 更新订单信息（更新订单状态)
    def put(self, request, order_id):
        url = order_url + '/' + str(order_id)
        status_id = request.data.get('status_id')
        order_query = Orders.objects.filter(bc_order_id=order_id)

        if not order_query.exists():
            return Response({
                'code': 400,
                'msg': 'Invalid order id'
            }, status=status.HTTP_400_BAD_REQUEST)

        result = requests.put(url=url, headers=headers, data=json.dumps(request.data))

        if result.status_code == 200:
            order = order_query.first()
            order.status = status_id
            order.save()

            return Response({
                'code': 200,
                'msg': 'Update success'
            })
        else:
            return Response(result.json(), status=result.status_code)
