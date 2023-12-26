from django.shortcuts import render
from .models import Ratings
from .serializers import RatingsSerializer
from recipes.models import Recipes
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F, Q

# --------------------- RATING ---------------------
@api_view(['POST'])
@csrf_exempt
def api_add_rating(request):
    try:
        user_id = request.data.get('user_id')
        recipe_id = request.data.get('recipe_id')

        if Ratings.objects.filter(user=user_id, recipe=recipe_id).exists():
            return Response({"message": "Rating already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingsSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer)
            rating_instance = serializer.save()

            recipe = Recipes.objects.get(recipe_id=recipe_id)
            recipe.rating_sum = F('rating_sum') + rating_instance.value
            recipe.rating_num = F('rating_num') + 1
            recipe.save()

            return Response({"message": "Rating added successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Rating couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@csrf_exempt
def api_remove_rating(request):
    try:
        recipe_id = request.data.get('recipe_id')
        user_id = request.data.get('user_id')
        
        rating_instance = Ratings.objects.get(Q(user = user_id) & Q(recipe = recipe_id))
        rating_instance.delete()

        recipe = Recipes.objects.get(recipe_id=recipe_id)
        recipe.rating_sum = F('rating_sum') - rating_instance.value
        recipe.rating_num = F('rating_num') - 1
        recipe.save()

        return Response({"message": "Rating deleted successfully"}, status=status.HTTP_200_OK)
    except Ratings.DoesNotExist:
        return Response({"message": "Rating not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response({"message": f"Rating couldn't be deleted: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

