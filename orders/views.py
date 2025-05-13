from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from cart.models import Cart
from .models import Order, OrderItem
from customer.models import Customer, Address
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer,OrderItemSerializer



class PlaceOrderView(APIView):
    def post(self, request):
        data = request.data
        required_fields = ['customer_id', 'items', 'address_id', 'order_total', 'order_status', 'payment_type']

        for field in required_fields:
            if field not in data:
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(customer_id=data['customer_id'])
        except Customer.DoesNotExist:
            return Response({'error': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = Address.objects.get(id=data['address_id'])
        except Address.DoesNotExist:
            return Response({'error': 'Invalid address_id'}, status=status.HTTP_400_BAD_REQUEST)

        items = data['items']
        if not isinstance(items, list) or not items:
            return Response({'error': 'Items must be a non-empty list'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create the Order
            new_order = Order.objects.create(
                customer_id=customer,
                address_id=address,
                order_total=data['order_total'],
                order_status=data['order_status'],
                payment_type=data['payment_type'],
            )

            for item in items:
                try:
                    product = Product.objects.get(product_id=item['product_id'])
                except Product.DoesNotExist:
                    return Response({'error': f'Invalid product_id: {item["product_id"]}'}, status=status.HTTP_400_BAD_REQUEST)

                quantity = item.get('quantity', 1)
                if quantity < 1:
                    return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

                OrderItem.objects.create(
                    order=new_order,
                    product_id=product,
                    quantity=quantity
                )

            # Clear the user's cart
            Cart.objects.filter(customer_id=customer).delete()

        return Response({'order_id': new_order.order_id}, status=status.HTTP_201_CREATED)

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CustomerOrdersView(APIView):
    def get(self, request, customer_id):
        orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateOrderStatusView(APIView):
    def patch(self, request, order_id):
        status_value = request.data.get('order_status')
        if not status_value:
            return Response({'error': 'order_status is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_id=order_id)
            order.order_status = status_value
            order.save()
            return Response({'message': 'Order status updated'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class DeleteOrderView(APIView):
    def delete(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            order.delete()
            return Response({'message': 'Order deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderItemsView(APIView):
    def get(self, request, order_id):
        items = OrderItem.objects.filter(order__order_id=order_id)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
