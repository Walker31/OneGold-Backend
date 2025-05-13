from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # List all products
    path('add/', views.add_product, name='add_product'),  # Add a new product
    path('update/<int:product_id>/', views.update_product, name='update_product'),  # Update product info
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),  # Delete a product
    path('filter/', views.filter_products, name='filter_products'),  # Filter products
    path('addreview',views.add_review,name='addReview'),
    path('getreviews',views.get_reviews,name= 'getReviews'),
    path('deleteReview',views.delete_review,name='deleteReview'),
    path('addwishlist',views.add_to_wishlist,name= 'addToWishlist'),
    path('removewishlist',views.remove_from_wishlist,name= 'removeFromWishlist'),
    path('<int:product_id>/', views.get_product_by_id, name='get_product_by_id'),
]
