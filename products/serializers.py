from .models import Products, Categories
from rest_framework import serializers


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['name', 'parent_id', 'bc_cate_id']


class ProductSerializers(serializers.ModelSerializer):

    class Meta:
        model = Products
        exclude = ['create_at', 'update_at']
