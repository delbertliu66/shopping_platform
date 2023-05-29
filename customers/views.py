from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CustomerSerializer
from customers.models import Customers


# Create your views here.
class CustomersView(APIView):
    def get(self, requset):
        customers = Customers.objects.all()
        customers_data = CustomerSerializer(customers, many=True).data
        return Response({
            'code': 200,
            'msg': 'success',
            'data': {
                'list': customers_data
            }
        })

