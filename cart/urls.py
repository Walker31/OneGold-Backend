from django.urls import path
from .views import AddToCartView, UpdateCartView, ViewCartView, ViewAllCartsView

urlpatterns = [
    path('add/', AddToCartView.as_view()),
    path('update/', UpdateCartView.as_view()),
    path('view/', ViewCartView.as_view()),
    path('all/', ViewAllCartsView.as_view()),  # For admin
]
