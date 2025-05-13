from django.http import JsonResponse
from .models import Category

def get_all_categories(request):
    # Retrieve all categories
    categories = Category.objects.all()
    
    # Prepare the data to return
    categories_data = list(categories.values('category_id', 'category_name'))
    
    # Return the categories as a JSON response
    return JsonResponse({'categories': categories_data})

def get_category_by_id(request, category_id):
    try:
        # Retrieve the category by category_id
        category = Category.objects.get(category_id=category_id)
        
        # Return the category name as a JSON response
        return JsonResponse({'category_name': category.category_name})
    
    except Category.DoesNotExist:
        # If category doesn't exist, return an error message
        return JsonResponse({'error': 'Category not found'}, status=404)