from django.urls import path
from .views import OrdersView, OrderDetailsView
urlpatterns = [
    path('orders', OrdersView.as_view()),
    path('orders/<int:order_id>', OrderDetailsView.as_view()),
]
