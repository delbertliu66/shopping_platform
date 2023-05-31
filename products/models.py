from unicodedata import category

from django.db import models
from utils.base_model import BaseModel


class Categories(BaseModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    parent_id = models.IntegerField(default=0)
    bc_cate_id = models.IntegerField(blank=False, null=False, unique=True)

    class META:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Products(BaseModel):
    name = models.CharField(max_length=200, blank=False, null=False)
    type = models.CharField(max_length=200, blank=False, null=False)    # bc 中只有 digital 和 physical两种选项
    weight = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False, default=35)
    sku = models.CharField(max_length=20, blank=True, null=False)
    bc_pro_id = models.IntegerField(null=False, blank=True, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products', to_field='bc_cate_id')

    class META:
        db_table = 'products'
        verbose_name = 'product'
        verbose_name_plural = 'products'

