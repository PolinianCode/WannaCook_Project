from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Recipes, RecipeIngredient
from .serializers import RecipesSerializer, RecipeIngredientSerializer
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import F
from django.utils import timezone


# --------------------- RECIPE ---------------------
# This section contains API endpoints related to recipe operations.

# Add recipe
@api_view(['POST'])
@csrf_exempt
def api_add_recipe(request):
    try:
        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        ingredients_data = request.data.get('ingredients', [])

        serializer = RecipesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_date'] = formatted_datetime
        with transaction.atomic():
            if serializer.is_valid():
                recipe_instance = serializer.save()

                for ingredient_data in ingredients_data:
                    ingredient_data['recipe'] = recipe_instance.recipe_id  
                    ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data)
                    ingredient_serializer.is_valid(raise_exception=True)
                    ingredient_serializer.save()

            return Response({"message": "The recipe has been added successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Recipe couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Get recipe data by id
@api_view(['GET'])
@csrf_exempt
def api_get_recipe(request):
    try:
        recipe_id = request.data.get('recipe_id')
        recipe = get_object_or_404(Recipes, recipe_id=recipe_id)
        serializer = RecipesSerializer(recipe)

        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        ingredients_serializer = RecipeIngredientSerializer(ingredients, many=True)

        response_data = {
            "recipe": serializer.data,
            "ingredients": ingredients_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Recipe {recipe_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

# Modify Recipe
@csrf_exempt
@api_view(['PUT'])
def api_modify_recipe(request):
    try:
        recipe_id = request.data.get("recipe_id")

        recipe = get_object_or_404(Recipes, pk=recipe_id)

        RecipeIngredient.objects.filter(recipe=recipe).delete()

        serializer = RecipesSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid():
            recipe_instance = serializer.save()

            ingredients_data = request.data.get('ingredients', [])
            for ingredient_data in ingredients_data:
                ingredient_data['recipe'] = recipe_instance.recipe_id
                ingredient_serializer = RecipeIngredientSerializer(data=ingredient_data)
                ingredient_serializer.is_valid(raise_exception=True)
                ingredient_serializer.save()

            return Response({"message": "The recipe has been modified successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Recipe modification failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete a recipe from the database.
@csrf_exempt
@api_view(['DELETE'])
def api_delete_recipe(request):
    try:
        recipe_id = request.data.get('recipe_id')

        recipe = get_object_or_404(Recipes, recipe_id=recipe_id)

        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        ingredients.delete()

        recipe.delete()

        return Response({"message": f"Recipe {recipe_id} and its ingredients have been deleted."}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"Recipe {recipe_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

#Get all recipes
@csrf_exempt
@api_view(['GET'])
def api_get_recipes(request):
    all_recipes = Recipes.objects.order_by("created_date")
    serializedRecipes = RecipesSerializer(all_recipes, many=True)
    return Response({'Recipes': serializedRecipes.data}, status=status.HTTP_200_OK)