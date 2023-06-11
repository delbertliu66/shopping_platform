from rest_framework import serializers
from .models import Customers
from addresses.serializers import PartialAddressesSerializer


class CustomerSerializer(serializers.ModelSerializer):

    address = serializers.SerializerMethodField()

    class Meta:
        fields = ['bc_id', 'first_name', 'last_name', 'email', 'address']
        model = Customers

    def get_address(self, obj):
        addresses_query = obj.address.all()
        # addresses = []
        # for address in addresses_query:
        #     addresses.append(address)
        address_data = PartialAddressesSerializer(addresses_query, many=True).data
        return address_data
