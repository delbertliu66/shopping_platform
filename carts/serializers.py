from rest_framework import serializers
from .models import Carts, CartItems
from customers.serializers import PartialCustomerSerializer, CustomerSerializer


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItems
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    customer = PartialCustomerSerializer()
    items = CartItemSerializer(many=True)

    class Meta:
        model = Carts
        fields = '__all__'
