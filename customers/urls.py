from django.urls import path
from .views import CustomersView

urlpatterns = [
    path('customers/', CustomersView.as_view()),

]
