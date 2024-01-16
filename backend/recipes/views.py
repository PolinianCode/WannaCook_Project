from rest_framework import viewsets
from .models import Recipes
from .serializers import RecipesSerializer
from ingredients.models import RecipeIngredient
from ingredients.serializers import RecipeIngredientSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action



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
        
    @action(detail=False, methods=['GET'])
    def get_recipes_by_user_id(self, request, user_id=None):
        try:
            recipes = Recipes.objects.filter(user__id=user_id)
            serializer = self.get_serializer(recipes, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Error getting recipes by user_id"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])    
    def get_homepage_recipes(self, request):
        try:
            queryset = Recipes.objects.all().order_by('-created_date')[:3]
            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Error getting recipes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
