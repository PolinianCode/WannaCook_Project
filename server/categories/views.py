from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Categories
from .serializers import CategoriesSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404

# --------------------- CATEGORIES ---------------------
# This section contains API endpoints related to user/recipe utils.


# Get all recipe categories from the database.
@api_view(['GET'])
@csrf_exempt
def api_load_recipe_categories(request):
    all_categories = Categories.objects.order_by('-id')
    serialized_categories = CategoriesSerializer(all_categories, many=True)
    return Response({'Categories': serialized_categories.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def api_add_category(request):
    try:
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category added successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Category couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['DELETE'])
def api_delete_category(request):
    try:
        category_id = request.data.get('category_id')
        category = get_object_or_404(Categories, id=category_id)
        category.delete()
        return Response({"message": f"Category {category_id} has been deleted."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Category {category_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


