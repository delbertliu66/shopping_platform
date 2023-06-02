from django.urls import path
from .views import CartsView,CartItemsView

urlpatterns = [
    path('carts/', CartsView.as_view()),
    path('carts/items/', CartsView.as_view()),
]
