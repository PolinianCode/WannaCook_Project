from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Ingredients
from .serializers import IngredientsSerializer


# --------------------- INGREDIENTS ---------------------
@api_view(['GET'])
@csrf_exempt    
def api_load_recipe_ingredients(request):
    try:
        ingredients = Ingredients.objects.order_by('name')
        serialized_ingredients = IngredientsSerializer(ingredients, many=True)
        return Response({'Ingredients': serialized_ingredients.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
def api_add_ingredient(request):
    try:
        serializer = IngredientsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ingredient added successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Ingredient couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@csrf_exempt
def api_delete_ingredient(request):
    try:
        ingredient_id = request.data.get('ingredient_id')
        ingredient = get_object_or_404(Ingredients, id=ingredient_id)
        ingredient.delete()
        return Response({"message": f"Ingredient {ingredient_id} has been deleted."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Ingredient {ingredient_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    

