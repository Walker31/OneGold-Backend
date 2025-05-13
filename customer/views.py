from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Customer, Address
from orders.models import Order
from products.views import get_wishlist_products
from .serializers import AddressSerializer
import random
import string

class LoginCustomerView(APIView):
    def post(self, request):
        phone_no = request.data.get('phone_no')
        password = request.data.get('password')

        customer = Customer.objects.filter(phone_no=phone_no).first()
        if not customer or not customer.user:
            return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=customer.user.username, password=password)
        if user:
            login(request, user)
            return Response({
                'message': 'Login successful',
                'customer_id': customer.customer_id,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)


class SignupCustomerView(APIView):
    def post(self, request):
        first_name = request.data.get('username')
        password = request.data.get('password')
        phone_no = request.data.get('phone_no')

        if Customer.objects.filter(phone_no=phone_no).exists():
            return Response({"error": "Phone Number already in use"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            while True:
                random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                generated_username = f"{first_name.lower()}{random_suffix}"
                if not User.objects.filter(username=generated_username).exists():
                    break

            user = User.objects.create_user(username=generated_username, password=password, first_name=first_name)
            customer = Customer(user=user, phone_no=phone_no)
            customer.save()

            return Response({
                "message": f"Customer created successfully. Welcome, {first_name}!",
                "username": generated_username
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred during signup: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutCustomerView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class CustomerProfileView(APIView):
    def get(self, request):
        customer_id = request.GET.get('customer_id')
        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customer, customer_id=customer_id)
        delivered_orders = Order.objects.filter(customer_id=customer_id, order_status="Delivered")

        customer_data = {
            "customer_id": customer.customer_id,
            "name": customer.user.username,
            "email": customer.email,
            "phone_no": customer.phone_no,
            "updated_at": customer.updated_at,
            "created_at": customer.created_at,
            "previous_orders": [],
            "wishlist": get_wishlist_products(customer_id),
        }

        for order in delivered_orders:
            for item in order.order_items.all():
                product = item.product
                product_info = {
                    "product_id": product.product_id,
                    "name": product.product_name,
                    "description": product.product_description,
                    "price": product.product_price,
                    "image": product.product_images,
                    "quantity": item.quantity,
                    "status": order.order_status,
                }
                customer_data["previous_orders"].append(product_info)

        return Response(customer_data, status=status.HTTP_200_OK)

class AddAddressView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        data_fields = ['pincode', 'city', 'state', 'location', 'landmark']
        data = {field: request.data.get(field) for field in data_fields}

        try:
            customer = get_object_or_404(Customer, customer_id=customer_id)
            address = Address(customer=customer, **data)
            address.save()
            return Response({"message": "Address saved successfully and linked to customer."}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "An error occurred during adding address."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class DeleteAddressView(APIView):
    def delete(self, request):
        customer_id = request.GET.get('customer_id')
        address_id = request.GET.get('address_id')

        if not customer_id or not address_id:
            return Response({"error": "customer_id and address_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address = get_object_or_404(Address, id=address_id, customer_id=customer_id)
            address.delete()
            return Response({"message": "Address deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred while deleting the address: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAddressesByCustomerView(APIView):
    def get(self, request):
        customer_id = request.query_params.get('customer_id')
        if not customer_id:
            return Response({"error": "Customer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(customer_id=customer_id)
            addresses = customer.addresses.all()
            if addresses.exists():
                serializer = AddressSerializer(addresses, many=True)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No addresses exist for this customer", "data": []}, status=status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateAddressView(APIView):
    def put(self, request):
        customer_id = request.data.get('customer')
        address_id = request.data.get('address_id')
        fields_to_update = ['pincode', 'city', 'state', 'location', 'landmark']

        try:
            address = get_object_or_404(Address, address_id=address_id, customer_id=customer_id)
            for field in fields_to_update:
                value = request.data.get(field)
                if value:
                    setattr(address, field, value)
            address.save()
            return Response({"message": "Address updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
