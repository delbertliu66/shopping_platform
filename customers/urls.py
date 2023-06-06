from django.urls import path
from .views import CustomersView, CustomerLoginView

urlpatterns = [
    path('customers', CustomersView.as_view(), name='customers'),
    path('login', CustomerLoginView.as_view())

]
