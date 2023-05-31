from django.urls import path
from .views import ProductsView,CategoriesView
urlpatterns = [
    path('products/', ProductsView.as_view()),
    path('categories/', CategoriesView.as_view())
]
