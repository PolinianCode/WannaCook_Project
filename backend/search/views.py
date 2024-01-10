from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from recipes.models import Recipes
from ingredients.models import RecipeIngredient
from recipes.serializers import RecipesSerializer

@csrf_exempt
def search_recipes(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        category = request.GET.get('category')
        user = request.GET.get('user')
        ingredient = request.GET.getlist('ingredients')

        filters = {}
        if title:
            filters['title__icontains'] = title
        if category:
            filters['category__id'] = category
        if user:
            filters['user__nickname__icontains'] = user
        if ingredient:
            recipes_with_ingredients = RecipeIngredient.objects.filter(ingredient_id__in=ingredient).values_list('recipe_id', flat=True)
            filters['id__in'] = recipes_with_ingredients

        search_results = Recipes.objects.filter(**filters)

        serialized_results = RecipesSerializer(search_results, many=True)

        return JsonResponse({"search_results": serialized_results.data}, status=200)
