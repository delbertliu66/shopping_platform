from rest_framework import serializers
from .models import Addresses


class PartialAddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Addresses
        exclude = ['create_at', 'update_at']
        # fields = '__all__'


class FullAddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Addresses
        fields = '__all__'
