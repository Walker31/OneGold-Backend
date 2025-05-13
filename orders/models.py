from django.db import models
from django.db.models import UniqueConstraint

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column='customer_id', default=1)  # Default customer_id (assuming 1 is a valid ID)
    address_id = models.ForeignKey('customer.Address',on_delete=models.CASCADE,db_column='address_id',default=1)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Default total as 0.00
    order_status = models.CharField(max_length=255, default='Pending')  # Default status as 'Pending'
    payment_type = models.CharField(max_length=255, default='Unspecified')  # Default payment type
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'  # This maps to the PostgreSQL table name
        managed = True  # Allows Django to manage this table (remove if not needed)

    def __str__(self):
        return f"Order ID: {self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE, default=1)  # Default order ID (assuming 1 is valid)
    product_id = models.ForeignKey('products.Product', on_delete=models.CASCADE, db_column='product_id', default=1)  # Default product ID
    quantity = models.PositiveIntegerField(default=1)  # Default quantity as 1

    class Meta:
        db_table = 'order_items'
        constraints = [
            UniqueConstraint(fields=['order', 'product_id'], name='unique_order_product')
        ]  # Ensure unique product for each order

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product_id}"
