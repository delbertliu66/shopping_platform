from django.db import models
from utils.base_model import BaseModel
from customers.models import Customers


class Addresses(BaseModel):
    address_id = models.IntegerField(unique=True)
    address1 = models.CharField(max_length=200, blank=False, null=False)
    address2 = models.CharField(max_length=200)
    address_type = models.CharField(max_length=200, blank=False, null=False)
    city = models.CharField(max_length=200, blank=False, null=False)
    company = models.CharField(max_length=200)
    country_code = models.CharField(max_length=200, blank=False, null=False)
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    phone = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200, blank=False, null=False)
    state_or_province = models.CharField(max_length=200, blank=False, null=False)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name='address', to_field='bc_id')

    class META:
        db_table = 'address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

