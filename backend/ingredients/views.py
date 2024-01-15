from rest_framework import viewsets
from .models import Ingredients, RecipeIngredient
from .serializers import IngredientsSerializer, RecipeIngredientSerializer
from rest_framework.response import Response
from rest_framework import status


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    def delete_all_by_recipe_id(self, request, recipe_id=None):
        try:
            recipe_ingredients = RecipeIngredient.objects.filter(recipe__id=recipe_id)
            if recipe_ingredients:
                recipe_ingredients.delete()
                return Response({"message": "Recipe ingredients deleted"}, status=status.HTTP_200_OK)
            return Response({"message": "Recipe ingredients don't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return False

