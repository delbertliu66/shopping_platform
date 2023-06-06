from django.urls import path
from .views import AddressesView

urlpatterns = [
    path('customers/addresses', AddressesView.as_view()),
]
