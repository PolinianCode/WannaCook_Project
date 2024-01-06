from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .models import Favorites
from .serializers import FavoritesSerializer


# --------------------- FAVORITES ---------------------
# Remove recipe from favorites
@api_view(['GET'])
@csrf_exempt
def api_load_favorites(request):
    try:
        favorites = Favorites.objects.filter(user = request.data.get('user_id')).order_by('-id')
        serialized_favorites = FavoritesSerializer(favorites, many=True)
        return Response({'Favorites': serialized_favorites.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Add recipe to favorites
@api_view(['POST'])
@csrf_exempt
def api_add_favorite(request):
    try:
        user_id = request.data.get('user')
        recipe_id = request.data.get('recipe')

        if user_id is None or recipe_id is None:
            return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)

        if Favorites.objects.filter(user=user_id, recipe=recipe_id).exists():
            return Response({"message": "Favorite already exists"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Recipe added to favorites successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Remove recipe to favorites
@api_view(['DELETE'])
@csrf_exempt
def api_remove_favorite(request):
    try:

        user_id = request.data.get('user_id')
        recipe_id = request.data.get('recipe_id')


        if user_id is None or recipe_id is None:
            return Response({"message": "Favorite remove error"}, status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorites.objects.filter(user = user_id, recipe = recipe_id)

        if favorite:
            favorite.delete()
        else:
            return Response({"message": f"Favorite for user {user_id} and recipe {recipe_id} has not been deleted."}, status=status.HTTP_404_NOT_FOUND)
        

        return Response({"message": f"Favorite for user {user_id} and recipe {recipe_id} has been deleted."}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"Favorite for user {user_id} and recipe {recipe_id} has not been deleted."}, status=status.HTTP_404_NOT_FOUND)

