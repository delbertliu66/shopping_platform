from django.db import models
from utils.base_model import BaseModel


# Create your models here.
class Customers(BaseModel):
    first_name = models.CharField(max_length=200, blank=False, null=False)
    last_name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    company = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    new_password = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        db_table = 'customers'
        verbose_name = 'customers'
        verbose_name_plural = 'customers'

