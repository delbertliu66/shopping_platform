from rest_framework import serializers
from .models import Addresses


class AddressesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Addresses
        exclude = ['create_at', 'update_at']
        # fields = '__all__'
