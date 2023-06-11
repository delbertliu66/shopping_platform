from .models import OrderItems, Orders
from rest_framework import serializers


class OrderItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = OrderItems
        exclude = ['create_at', 'update_at', 'id']


class OrderSerializers(serializers.ModelSerializer):

    items = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = '__all__'

    def get_items(self, obj):
        order_items = OrderItems.objects.filter(order=obj)
        order_data = OrderItemSerializers(order_items, many=True).data
        return order_data
