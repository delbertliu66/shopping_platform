import time

import jwt
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from shopping_platform import settings
from .serializers import CustomerSerializer
from customers.models import Customers


# Create your views here.
class CustomersView(APIView):

    # 获取消费者列表
    def get(self, requset):
        customers = Customers.objects.all()
        # 上一句得到的结果为查询集，需要通过序列化得到数据
        customers_data = CustomerSerializer(customers, many=True).data
        # 返回固定格式
        return Response({
            'code': 200,
            'msg': 'success',
            'data': {
                'list': customers_data
            }
        })


class CustomerLoginView(APIView):

    # 消费者登录，下发token
    def post(self, request):
        login_data = request.data

        # 通过用户输入的邮箱和密码，判断是否输入正确
        customer = Customers.objects.filter(
            email=login_data['email'],
            new_password=login_data['new_password']
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
