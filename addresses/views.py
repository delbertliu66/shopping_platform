from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests


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
