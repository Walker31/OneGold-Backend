from django.urls import path
from . import views

urlpatterns = [
    path('',views.get_all_categories,name = 'get_categories')
]