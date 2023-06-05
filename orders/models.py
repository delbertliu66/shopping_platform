from django.db import models
from utils.base_model import BaseModel
from customers.models import Customers
from products.models import Products
from addresses.models import Addresses


ORDER_STATUS_CHOICES = [
    (0, 'Incomplete'),
    (1, 'Pending'),
    (2, 'Shipped'),
    (3, 'Partially Shipped'),
    (4, 'Refunded'),
    (5, 'Cancelled'),
    (6, 'Declined'),
    (7, 'Awaiting Payment'),
    (8, 'Awaiting Pickup'),
    (9, 'Awaiting Shipment'),
    (10, 'Completed'),
    (11, 'Awaiting Fulfillment'),
    (12, 'Manual Verification Required'),
    (13, 'Disputed'),
    (14, 'Partially Refunded')
]


class Orders(BaseModel):
    bc_order_id = models.IntegerField(default=0, unique=True)
    customer = models.ForeignKey(Customers, related_name='orders', on_delete=models.CASCADE, to_field='bc_id')
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_quantity = models.PositiveIntegerField(default=1)
    address = models.ForeignKey(Addresses, on_delete=models.DO_NOTHING, to_field='address_id')

    def update_quantity_price(self):
        order_items = self.items.all()
        total_quantity = 0
        total_price = 0

        for order_item in order_items:
            total_quantity += order_item.quantity
            total_price += order_item.total_price

        self.total_quantity = total_quantity
        self.total_price = total_price
        self.save()

    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'


class OrderItems(BaseModel):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE, to_field='bc_order_id')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, to_field='bc_pro_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'order_item'
        verbose_name_plural = 'order_items'
