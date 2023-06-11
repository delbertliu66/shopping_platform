from django.urls import path
from .views import AddressesView, AddressDetailsView

urlpatterns = [
    path('customers/addresses', AddressesView.as_view()),
    path('customers/address/details', AddressDetailsView.as_view())
]
