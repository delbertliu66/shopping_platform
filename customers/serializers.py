from rest_framework import serializers
from .models import Customers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['bc_id', 'first_name', 'last_name', 'email']
        model = Customers
