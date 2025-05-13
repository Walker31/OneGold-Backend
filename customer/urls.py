from django.urls import path
from .views import (
    LoginCustomerView, SignupCustomerView, LogoutCustomerView,
    CustomerProfileView, AddAddressView, DeleteAddressView,
    GetAddressesByCustomerView, UpdateAddressView
)

urlpatterns = [
    path('login/', LoginCustomerView.as_view()),
    path('signup/', SignupCustomerView.as_view()),
    path('logout/', LogoutCustomerView.as_view()),
    path('profile/', CustomerProfileView.as_view()),
    path('add-address/', AddAddressView.as_view()),
    path('delete-address/', DeleteAddressView.as_view()),
    path('get-addresses/', GetAddressesByCustomerView.as_view()),
    path('update-address/', UpdateAddressView.as_view()),
]
