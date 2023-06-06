import json
import time

import jwt
import requests
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

customer_url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers'


def create_customer_in_local_database(customer_data, bc_id):
    new_customer = Customers.objects.create(
        first_name=customer_data['first_name'],
        last_name=customer_data['last_name'],
        email=customer_data['email'],
        phone=customer_data['phone'],
        company=customer_data['company'],
        new_password=customer_data.get('authentication', {}).get('new_password'),
        bc_id=bc_id
    )
    return new_customer


# Create your views here.
class CustomersView(APIView):

    # 获取消费者列表（从bc官方获取）
    def get(self, requset):

        # 从bc官方获取消费者数据
        result = requests.get(customer_url, headers=headers)
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
        # 获取request作用域中的值（引用）
        customer_data = requset.data

        # 将新增的消费者上传到bc店铺的数据库
        result = requests.post(customer_url, data=json.dumps([customer_data]), headers=headers)
        response = result.json()

        if result.status_code == 200:
            # 如果保存到bc店铺成功，则创建并保存新的消费者对象到本地数据库
            new_customer = create_customer_in_local_database(customer_data, response['data'][0].get('id'))
            # 成功返回
            return Response({
                'code': 200,
                'msg': 'add success',
                'data': response['data'][0]
            })

        # 失败返回
        else:
            return Response(response, status=result.status_code)

    # 更新消费者， 需要在request请求体中填写bc店铺的customer的id
    def put(self, request):
        new_data = request.data
        bc_id_up = request.query_params.get('bc_id')

        # 查询是否具有bc_id 等于 bc_id_up的customer（用bc_id是为了方便在bc店铺数据库中修改数据）
        try:
            customer = Customers.objects.get(bc_id=bc_id_up)
        except Customers.DoesNotExist:
            # 如果不存在此customer，则返回错误信息
            return Response({
                'code': 404,
                'msg': 'Customer not found!'
            }, status=status.HTTP_404_NOT_FOUND)
        # 如果存在用户则，更新用户信息，先更细bc店铺的数据
        url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers'
        result = requests.put(url, data=json.dumps([request.data]), headers=headers)

        # 返回
        if result.status_code == 200:

            new_password = new_data.get('authentication', {}).get('new_password')
            if new_password is not None:
                customer.new_password = new_password
            new_data.pop('id', None)
            # 优化代码
            for key, value in new_data.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)

            # 更新本地数据库
            # if 'first_name' in new_data:
            #     customer.first_name = new_data['first_name']
            # if 'last_name' in new_data:
            #     customer.last_name = new_data['last_name']
            # if 'phone' in new_data:
            #     customer.phone = new_data['phone']
            # if 'company' in new_data:
            #     customer.company = new_data['company']
            # if 'authentication' in new_data:
            #     customer.new_password = new_data.get('authentication', {}).get('new_password')
            # 保存修改后的信息

            customer.save()

            return Response({
                'code': 200,
                'msg': 'update success!',
                'data': result.json()['data'][0]
            })
        else:
            return Response(result.json(), status=result.status_code)

    # 删除消费者，需要在路径参数中携带需要删除的id（bc店铺存储的id），查询参数为id:in=4,5,6
    def delete(self, request):
        # 从参数中将bc_id列表提取出来
        bc_ids = request.query_params['ids']
        # 将id_param划分为一个id列表
        id_list = [int(id_) for id_ in bc_ids.split(',')]
        # 删除指定的id用户（在本地是bc_id）

        customers = Customers.objects.filter(bc_id__in=id_list)
        # 判断要删除的用户是否存在
        if customers.exists():
            # 如果存在，删除bc店铺的数据，然后删除本地数据库的数据
            url = 'https://api.bigcommerce.com/stores/rmz2xgu42d/v3/customers?id:in={}'.format(','.join(
                str(_id) for _id in id_list))
            result = requests.delete(url, headers=headers)

            if result.status_code == 204:
                customers.delete()
                return Response({
                    'code': 200,
                    'msg': 'delete success'
                }, status=result.status_code)
            else:
                return Response(result)
        else:
            return Response({
                'code': 404,
                'msg': "no customers!"
            }, status=status.HTTP_404_NOT_FOUND)


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
            'exp': int(time.time()) + 60 * 60 * 24 * 7
        }

        # 使用jwt加密信息
        token = jwt.encode(payload, settings.SECRET_KEY)

        # 下发token
        return Response({
            'code': 200,
            'msg': "Login success, Issued token",
            'token': token,
        })
