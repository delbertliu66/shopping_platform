from django.db import models

from customers.models import Customers
from utils.base_model import BaseModel

from products.models import Products


class Carts(BaseModel):
    total_quantity = models.PositiveIntegerField(default=0)     # 购物车中商品数量，默认为0
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)    # 购物车商品总价，最大位数10，两位小数，默认0.00
    customer = models.ForeignKey(Customers, related_name='cart', on_delete=models.CASCADE, to_field='bc_id')

    def update_total(self):
        cart_items = self.items.all()
        total_quantity = 0
        total_price = 0

        for cart_item in cart_items:
            total_quantity += cart_item.quantity
            total_price += cart_item.price * cart_item.quantity

        self.total_quantity = total_quantity
        self.total_price = total_price
        self.save()

    class Meta:
        db_table = 'carts'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'


class CartItems(BaseModel):
    cart = models.ForeignKey(Carts, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, to_field='bc_pro_id')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'items'
        verbose_name = 'item'
        verbose_name_plural = 'items'
