from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from recipes.models import Recipes
from recipes.serializers import RecipesSerializer

# --------------------- SEARCH ---------------------
    
# Serach recipes
@api_view(['GET'])
@csrf_exempt
def api_search_recipes(request):
    try:
        title = request.data.get("title", "")
        category = request.data.get("category", "")
        user = request.data.get("user", "")
        #ingredient = request.data.get("ingredient", "")

        filters = {}
        if title:
            filters['title__icontains'] = title
        if category:
            filters['category__id__icontains'] = category
        if user:
            filters['user__nickname__icontains'] = user

        search_results = Recipes.objects.filter(**filters)

        serialized_results = RecipesSerializer(search_results, many=True)

        return Response({"search_results": serialized_results.data}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"Search failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

