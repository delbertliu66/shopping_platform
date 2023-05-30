import json
import time

import jwt
import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from shopping_platform import settings
from .serializers import CustomerSerializer
from customers.models import Customers


headers = {
    "X-Auth-Token": "n4npdilxz1ckdibl3wo8d8yehx2hi3x",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


# Create your views here.
class CustomersView(APIView):

    # 获取消费者列表（从bc官方获取）
    def get(self, requset):
        # customers = Customers.objects.all()
        # # 上一句得到的结果为查询集，需要通过序列化得到数据
        # customers_data = CustomerSerializer(customers, many=True).data
        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers'
        # 从bc官方获取消费者数据
        result = requests.get(url, headers=headers)
        customers = result.json()['data']
        # 返回固定格式
        return Response({
            'code': 200,
            'msg': 'success',
            'data': {
                'customers': customers
            }
        })

    # 新增消费者（首先要保存到自己的数据库中，然后上传到bc官方数据库）
    def post(self, requset):
        # 获取request作用域中的值
        customer_data = requset.data[0]

        # 将新增的消费者上传到bc店铺的数据库
        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers'
        body = json.dumps(requset.data)
        result = requests.post(url, data=body, headers=headers)

        if result.status_code == 200:
            # 如果保存到bc店铺成功，则创建并保存新的消费者对象到本地数据库
            new_customer = Customers.objects.create(
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name'],
                email=customer_data['email'],
                phone=customer_data['phone'],
                company=customer_data['company'],
                new_password=customer_data.get('authentication', {}).get('new_password')
            )

        return Response(result.json())


class CustomerLoginView(APIView):
    # 跳过token验证
    authentication_classes = ()

    # 消费者登录，下发token
    def post(self, request):
        login_data = request.data

        # 通过用户输入的邮箱和密码，判断是否输入正确
        customer = Customers.objects.filter(
            email=login_data['email'],
            new_password=login_data['password']
        ).first()

        # 如果用户输入信息不正确，则返回相应状态码和错误信息
        if not customer:
            return Response({
                'code': 404,
                'msg': 'User not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # 如果用户输入信息正确，则下发token
        payload = {
            'email': customer.email,
            # 过期时间
            'exp': int(time.time()) + 60 * 60
        }

        # 使用jwt加密信息
        token = jwt.encode(payload, settings.SECRET_KEY)

        # 下发token
        return Response({
            'code': 200,
            'msg': "Login success, Issued token",
            'token': token,
        })
