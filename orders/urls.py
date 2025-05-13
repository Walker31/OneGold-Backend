from django.urls import path
from .views import (
    PlaceOrderView, OrderListView, CustomerOrdersView,
    OrderDetailView, UpdateOrderStatusView,
    DeleteOrderView, OrderItemsView
)

urlpatterns = [
    path('orders/place/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/', OrderListView.as_view(), name='all-orders'),
    path('orders/customer/<int:customer_id>/', CustomerOrdersView.as_view(), name='customer-orders'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update-status'),
    path('orders/<int:order_id>/delete/', DeleteOrderView.as_view(), name='delete-order'),
    path('orders/<int:order_id>/items/', OrderItemsView.as_view(), name='order-items'),
]
