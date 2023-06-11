from django.urls import path
from .views import ProductsView, CategoriesView, ProductDetailsView
urlpatterns = [
    path('products', ProductsView.as_view()),
    path('categories', CategoriesView.as_view()),
    path('product/details', ProductDetailsView.as_view()),
]
