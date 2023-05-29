from django.urls import path
from .views import CustomersView, CustomerLoginView

urlpatterns = [
    path('customers/', CustomersView.as_view()),
    path('login/', CustomerLoginView.as_view())

]
