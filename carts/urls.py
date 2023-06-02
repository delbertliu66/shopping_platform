from django.urls import path
from .views import CartsView,CartItemsView

urlpatterns = [
    path('carts/', CartsView.as_view()),
    path('carts/<int:cart_id>/items/', CartItemsView.as_view()),
]
