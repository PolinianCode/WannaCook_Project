from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Recipes, Users, Categories, Favorites, Comments
from .serializers import UsersSerializer, CommentsSerializer, CategoriesSerializer, RecipesSerializer, FavoritesSerializer
from rest_framework import status
from .utils import is_user_exists, is_email_taken, is_favorite_exists
from django.shortcuts import get_object_or_404

# --------------------- USER ---------------------
# This section contains API endpoints related to user operations.


# Get all users from database.
@api_view(['GET'])
@csrf_exempt
def api_get_users(request):
    all_users = Users.objects.order_by('-user_id')
    serialized_users = UsersSerializer(all_users, many=True)
    return Response({'latest_users': serialized_users.data}, status=status.HTTP_200_OK)


# Add a new user to the database.
@api_view(['POST'])
@csrf_exempt
def api_add_user(request):
    try:
        username_data = request.data.get('nickname', '')
        email_data = request.data.get('email', '')

        if not username_data:
            return Response({'error': 'Missing username parameter!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_user_exists(username_data):
            return Response({'error': 'User with this username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if is_email_taken(email_data):
            return Response({'error': 'Email is already taken!'}, status=status.HTTP_400_BAD_REQUEST)


        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")
        

        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['registration_date'] = formatted_datetime
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User has been created!'}, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@csrf_exempt
def api_get_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = Users.objects.filter(nickname=username, password=password).first()


    if user is not None:
        return Response({"message": "Login successfull"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)  

# Remove a user from the database by nickname.
@api_view(['DELETE'])
@csrf_exempt
def api_remove_user(request):
    try:

        username = request.data.get('username')

        user = get_object_or_404(Users, nickname=username)
        user.delete()
        return Response({"message": f"User {username} has been deleted."})
    except Exception as e:
        print(e)
        return Response({"message": f"User {username} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


# --------------------- RECIPE ---------------------
# This section contains API endpoints related to recipe operations.

# Add recipe
@api_view(['POST'])
@csrf_exempt
def api_add_recipe(request):
    try:

        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        serializer = RecipesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['created_date'] = formatted_datetime
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "The recipe has been added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Recipe couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Modify Recipe
@csrf_exempt
@api_view(['PUT'])
def api_modify_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipes, pk=recipe_id)
        serializer = RecipesSerializer(recipe, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
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

        recipe.delete()

        return Response({"message": f"Recipe {recipe_id} has been deleted."}, status=status.HTTP_200_OK)

     except Exception as e:
        print(e)
        return Response({"message": f"Recipe {recipe_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)



# --------------------- UTILS ---------------------
# This section contains API endpoints related to user/recipe utils.


# Get all recipe categories from the database.
@api_view(['GET'])
@csrf_exempt
def api_load_recipe_categories(request):
    all_categories = Categories.objects.order_by('-id')
    serialized_categories = CategoriesSerializer(all_categories, many=True)
    return Response({'Categories': serialized_categories.data}, status=status.HTTP_200_OK)

# Add recipe to favorites
@api_view(['POST'])
@csrf_exempt
def api_add_favorite(request):
    try:
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Recipe added to favorites successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Remove recipe from favorites
@api_view(['POST'])
@csrf_exempt
def api_remove_favorite(request):
    try:

        user_id = request.data.get('user_id')
        recipe_id = request.data.get('recipe_id')


        if user_id is None or recipe_id is None:
            return Response({"message": "Favorite remove error"}, status=status.HTTP_400_BAD_REQUEST)

        favorite = Favorites.objects.filter(user = user_id, recipe = recipe_id)

        favorite.delete()

        return Response({"message": f"Favorite for user {user_id} and recipe {recipe_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        print(e)
        return Response({"message": f"Favorite for user {user_id} and recipe {recipe_id} has been deleted."}, status=status.HTTP_404_NOT_FOUND)

# Add comment to recipe
@api_view(['POST'])
@csrf_exempt
def api_add_comment(request):
    try:
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Remove comment from recipe
@api_view(['DELETE'])
@csrf_exempt
def api_remove_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comments, pk=comment_id)
        comment.delete()

        return Response({"message": f"Comment {comment_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        print(e)
        return Response({"message": f"Comment {comment_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


# Edit comment 
@api_view(['PUT'])
@csrf_exempt
def api_modify_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comments, pk=comment_id)

        data = request.data
        comment_text_data = data.get('comment_text', comment.comment_text)

        comment.comment_text = comment_text_data
        comment.save()

        return Response({"message": f"Comment {comment_id} has been modified successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment modification failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get comments for recipe
@api_view(['GET'])
@csrf_exempt
def api_get_comments(request, recipe_id):
    recipe_comments = Comments.objects.order_by('-comment_date')
    serialized_comments = CommentsSerializer(recipe_comments, many=True)
    return Response({'Comments': serialized_comments.data}, status=status.HTTP_200_OK)

# --------------------- SEARCH ---------------------
# This section contains API endpoints related to search function.

@csrf_exempt
@api_view(['POST'])
def api_add_category(request):
    try:
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category added successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Category couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def api_get_recipes_by_category(request):
    try:
        category = request.data.get('category_id')
        recipes = Recipes.objects.filter(category=category)
        serialized_recipes = RecipesSerializer(recipes, many=True)
        return Response({'Recipes': serialized_recipes.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Recipe {category} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


