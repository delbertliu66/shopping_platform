import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from customers.models import Customers
from shopping_platform import settings


class JwtAuth(BaseAuthentication):

    def authenticate(self, requset):
        # 从request的Header中获取token
        token = requset.META.get('HTTP_TOKEN')
        # 解码token
        try:
            payload =jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except (jwt.DecodeError, jwt.InvalidSignatureError):
            raise AuthenticationFailed('Invalid Token')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Expired Token')
        # 成功解码从token中获取email
        email = payload['email']

        customer = cache.get(f'customer:{email}')
        if customer is not None:
            return customer, None

        # 根据邮箱查询是否存在用户
        customer = Customers.objects.filter(email=email).first()
        cache.set(f'customer:{customer.email}', customer, timeout=60 * 60 * 2)

        if not customer:
            raise AuthenticationFailed('Invalid Token')

        # 如果正确返回
        return customer, None


