from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Cart
from customer.models import Customer
from products.models import Product
from .serializers import CartSerializer
from products.serializers import ProductSerializer


class AddToCartView(APIView):
    def post(self, request):
        customer_id = request.query_params.get('customer_id')
        product_id = request.query_params.get('product_id')

        if not customer_id or not product_id:
            return Response({'error': 'customer_id and product_id are required'}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customer, pk=customer_id)
        product = get_object_or_404(Product, product_id=product_id)

        cart_item, created = Cart.objects.get_or_create(
            customer_id=customer, product_id=product,
            defaults={'qty': 1, 'total': product.product_price}
        )

        if not created:
            cart_item.qty += 1
            cart_item.total = cart_item.qty * product.product_price
            cart_item.save()

        return Response({
            'message': 'Product added to cart',
            'cart_item_qty': cart_item.qty,
            'cart_total': cart_item.total
        }, status=status.HTTP_200_OK)


class UpdateCartView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        product_id = request.data.get('product_id')
        action = request.data.get('action')

        if not all([customer_id, product_id, action]):
            return Response({'error': 'customer_id, product_id, and action are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart_item = Cart.objects.get(customer_id_id=customer_id, product_id_id=product_id)

            if action == 'increase':
                cart_item.qty += 1
            elif action == 'decrease':
                if cart_item.qty <= 1:
                    return Response({"error": "Quantity cannot be less than 1"}, status=status.HTTP_400_BAD_REQUEST)
                cart_item.qty -= 1
            elif action == 'delete':
                cart_item.delete()
                return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

            cart_item.total = cart_item.qty * cart_item.product_id.product_price
            cart_item.save()

            return Response({
                'message': 'Cart updated',
                'cart_item_qty': cart_item.qty,
                'cart_total': cart_item.total
            })

        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


class ViewCartView(APIView):
    def get(self, request):
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = Cart.objects.filter(customer_id_id=customer_id).select_related('product_id')

        total_cost = 0
        total_qty = 0
        cart_data = []

        for item in cart_items:
            total_cost += item.total
            total_qty += item.qty

            item_data = CartSerializer(item).data
            item_data['product'] = ProductSerializer(item.product_id).data
            cart_data.append(item_data)

        return Response({
            'cart_items': cart_data,
            'total_cost': total_cost,
            'total_qty': total_qty
        })


class ViewAllCartsView(APIView):
    def get(self, request):
        cart_items = Cart.objects.all().select_related('product_id', 'customer_id')
        serializer = CartSerializer(cart_items, many=True)
        total_cost = sum(item.total for item in cart_items)

        return Response({
            'cart_items': serializer.data,
            'total_cost': total_cost
        })
