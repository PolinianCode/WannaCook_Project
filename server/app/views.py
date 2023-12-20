from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Recipes, Users, Categories, Favorites, Comments, Ingredients, RecipeIngredient
from .serializers import UsersSerializer, CommentsSerializer, CategoriesSerializer, RecipesSerializer, FavoritesSerializer, IngredientsSerializer
from rest_framework import status
from .utils import is_user_exists, is_email_taken, is_favorite_exists
from django.shortcuts import get_object_or_404
from django.db.models import Q

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
    
# Get user data
@api_view(['GET'])
@csrf_exempt
def api_get_user(request):
    username = request.data.get('nickname')
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

        username = request.data.get('nickname')

        user = get_object_or_404(Users, nickname=username)
        user.delete()
        return Response({"message": f"User {username} has been deleted."})
    except Exception as e:
        print(e)
        return Response({"message": f"User {username} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
def api_modify_user(request):
    try:
        user_id = request.data.get("user_id")

        if user_id is None:
            return Response({"message": "Missing parameter"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Users, user_id=user_id)


        data = request.data
        nickname_data = data.get('nickname', user.nickname)
        email_data = data.get('email', user.email)


        user.nickname = nickname_data
        user.email = email_data


        user.save()

        return Response({"message": f"User {user_id} has been modified successfully"}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"User modification failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


@api_view(['GET'])
@csrf_exempt
def api_get_recipe(request):
    try:
        recipe_id = request.data.get('recipe_id')
        recipe = get_object_or_404(Recipes, recipe_id=recipe_id)
        serializer = RecipesSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)
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



# --------------------- CATEGORIES ---------------------
# This section contains API endpoints related to user/recipe utils.


# Get all recipe categories from the database.
@api_view(['GET'])
@csrf_exempt
def api_load_recipe_categories(request):
    all_categories = Categories.objects.order_by('-id')
    serialized_categories = CategoriesSerializer(all_categories, many=True)
    return Response({'Categories': serialized_categories.data}, status=status.HTTP_200_OK)


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
@api_view(['DELETE'])
def api_delete_category(request):
    try:
        category_id = request.data.get('category_id')
        category = get_object_or_404(Categories, id=category_id)
        category.delete()
        return Response({"message": f"Category {category_id} has been deleted."}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Category {category_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)



# Add recipe to favorites

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
            return Response({"message": "Ingredient added successfully"}, status=status.HTTP_201_CREATED)
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
    

# --------------------- SEARCH ---------------------
@api_view(['GET'])
@csrf_exempt
def api_search_recipes(request):
    try:
        title = request.data.get("title", "")
        category = request.data.get("category", "")
        user = request.data.get("user", "")
        #ingredient = request.data.get("ingredient", "")

        filters = {}
        if title:
            filters['title__icontains'] = title
        if category:
            filters['category__id__icontains'] = category
        if user:
            filters['user__nickname__icontains'] = user

        search_results = Recipes.objects.filter(**filters)

        serialized_results = RecipesSerializer(search_results, many=True)

        return Response({"search_results": serialized_results.data}, status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"message": f"Search failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------- FAVORITES ---------------------
# Remove recipe from favorites
@api_view(['GET'])
@csrf_exempt
def api_load_favorites(request):
    try:
        favorites = Favorites.objects.filter(user = request.data.get('user')).order_by('-id')
        serialized_favorites = FavoritesSerializer(favorites, many=True)
        return Response({'Favorites': serialized_favorites.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return Response({"message": "Recipe added to favorites successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

# --------------------- Comments ---------------------
# Add comment to recipe
@api_view(['POST'])
@csrf_exempt
def api_add_comment(request):
    try:

        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['comment_date'] = formatted_datetime
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Remove comment from recipe
@api_view(['DELETE'])
@csrf_exempt
def api_remove_comment(request):
    try:
        comment_id = request.data.get("comment_id")

        comment = get_object_or_404(Comments, pk=comment_id)
        comment.delete()

        return Response({"message": f"Comment {comment_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        print(e)
        return Response({"message": f"Comment {comment_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


# Edit comment 
@api_view(['PUT'])
@csrf_exempt
def api_modify_comment(request):
    try:
        comment_id = request.data.get("comment_id")  

        if comment_id is None:
            return Response({"message": "Comment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

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
def api_get_comments(request):
    try:
        recipe_id = request.data.get('recipe_id')
        comments = Comments.objects.filter(recipe=recipe_id).order_by('-id')
        serialized_comments = CommentsSerializer(comments, many=True)
        return Response({'Comments': serialized_comments.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

