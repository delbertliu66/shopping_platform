from rest_framework import serializers
from .models import Customers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Customers
