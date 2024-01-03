from urllib.parse import unquote_plus
import json

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from recipes.models import Recipes
from recipes.serializers import RecipesSerializer

from recipes.models import RecipeIngredient

# Search recipes
@csrf_exempt
@api_view(['GET'])
def api_search_recipes(request):
    try:
        encoded_data = request.GET.get('data', '')
        decoded_data = unquote_plus(encoded_data)

        data = json.loads(decoded_data)

        title = data.get("title", "")
        category = data.get("category", "")
        user = data.get("user", "")
        ingredient = data.get("ingredients", [])

        filters = {}
        if title:
            filters['title__icontains'] = title
        if category:
            filters['category__id__icontains'] = category
        if user:
            filters['user__nickname__icontains'] = user
        if ingredient:
            recipes_with_ingredients = RecipeIngredient.objects.filter(id__in = ingredient).values_list('recipe_id', flat=True)
            filters['recipe_id__in'] = recipes_with_ingredients

        search_results = Recipes.objects.filter(**filters)

        serialized_results = RecipesSerializer(search_results, many=True)

        return Response({"search_results": serialized_results.data}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"Search failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
