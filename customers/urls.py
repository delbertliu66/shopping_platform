from django.urls import path
from .views import CustomersView, CustomerLoginView, CustomerDetailView

urlpatterns = [
    path('customers', CustomersView.as_view(), name='customers'),
    path('login', CustomerLoginView.as_view()),
    path('customer/details', CustomerDetailView.as_view())

]
