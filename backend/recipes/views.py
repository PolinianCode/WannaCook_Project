from rest_framework import viewsets
from .models import Recipes
from .serializers import RecipesSerializer
from ingredients.models import RecipeIngredient
from ingredients.serializers import RecipeIngredientSerializer
from rest_framework.response import Response

#import status
from rest_framework import status


from django.shortcuts import get_object_or_404

class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            recipe = self.get_object()
            serializer = self.get_serializer(recipe)

            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            ingredients_serializer = RecipeIngredientSerializer(ingredients, many=True)

            response_data = {
                "recipe": serializer.data,
                "ingredients": ingredients_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Recipe doesn't exist"}, status=status.HTTP_404_NOT_FOUND)