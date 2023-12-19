from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.utils import timezone
from rest_framework.decorators import api_view
from .models import Recipes, Users, Categories, Favorites, Comments
from .serializers import UsersSerializer, CommentsSerializer, CategoriesSerializer
import json
from rest_framework import status
from .utils import check_user_exist, check_user_email_exist, check_user_favorites_exists
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
        nickname_data = request.data.get('nickname', '')
        email_data = request.data.get('email', '')
        password_data = request.data.get('password', '')
        is_moderator_data = request.data.get('is_moderator', '0')

        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        if not nickname_data or not email_data or not password_data:
            return Response({'error': 'Missing parameters!'}, status=status.HTTP_400_BAD_REQUEST)

        if check_user_exist(nickname_data) or check_user_email_exist(email_data):
            return Response({'error': 'User exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = Users(nickname=nickname_data, email=email_data, password=password_data, registration_date=formatted_datetime, is_moderator=is_moderator_data)
            user.save()

            return Response({'message': 'User has been created!'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Remove a user from the database by nickname.
@api_view(['DELETE'])
@csrf_exempt
def api_remove_user(request, username):
    try:
        user = get_object_or_404(Users, nickname=username)
        user.delete()
        return Response({"message": f"User {username} has been deleted."})
    except Exception as e:
        print(e)
        return Response({"message": f"User {username} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


# --------------------- RECIPE ---------------------
# This section contains API endpoints related to recipe operations.


# Add a new recipe to the database.
@api_view(['POST'])
@csrf_exempt
def api_add_recipe(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            title_data = data.get('title', '')
            description_data = data.get('description', '')
            instructions_data = data.get('instruction', '')
            user_id_data = data.get('user_id', None)
            category_name_data = data.get('category_id', '')

            current_datetime = timezone.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d")

            if user_id_data is None:
                return Response({"message": f"Missing user id"}, status=status.HTTP_400_BAD_REQUEST)

            if not title_data or not description_data or not instructions_data or not category_name_data:
                return Response({"message": f"Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = Users.objects.get(pk=user_id_data)
            category = Categories.objects.get(pk=category_name_data)
        
            recipe = Recipes(
                title=title_data,
                description=description_data,
                instruction=instructions_data,
                created_date=formatted_datetime,
                rating_sum=0,
                rating_num=0,
                category=category,
                user=user
            )
            recipe.save()

            return Response({"message": f"The recipe has been added successfully"}, status=status.HTTP_201_CREATED)

        
        else:
            return Response({'error': 'Request Error'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({"message": f"Recipe cant be added to DB {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Modify an existing recipe in the database.
@csrf_exempt
@api_view(['PUT'])
def api_modify_recipe(request, recipe_id):

    try:
        recipe = get_object_or_404(Recipes, pk=recipe_id)

        if request.method == "PUT":
            data = json.loads(request.body)
            title_data = data.get('title', recipe.title)
            description_data = data.get('description', recipe.description)
            instructions_data = data.get('instruction', recipe.instruction)
            category_name_data = data.get('category_id', recipe.category.id)

            
            recipe.title = title_data
            recipe.description = description_data
            recipe.instruction = instructions_data

           
            category = get_object_or_404(Categories, pk=category_name_data)
            recipe.category = category

            recipe.save()

            return Response({"message": f"The recipe has been modified successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Request Method'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({"message": f"Recipe modification failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete a recipe from the database.
@csrf_exempt
@api_view(['DELETE'])
def api_delete_recipe(request, recipe_id):
     try:
        recipe = get_object_or_404(Recipes, recipe_id=recipe_id)

        recipe.delete()

        return Response({"message": f"Recipe {recipe_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)

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

@api_view(['POST'])
@csrf_exempt
def api_add_favorite(request):
    try:
        if request.method == 'POST':
            data = request.data
            recipe_id_data = data.get('recipe_id', None)
            user_id_data = data.get('user_id', None)

            if not recipe_id_data or not user_id_data:
                return Response({"message": "Missing requirement parameters"}, status=status.HTTP_400_BAD_REQUEST)

            if check_user_favorites_exists(recipe_id_data, user_id_data):
                return Response({"message": "Recipe is already in the favorites list for this user"}, status=status.HTTP_200_OK)

            else:
                favorite = Favorites(recipe_id=recipe_id_data, user_id=user_id_data)
                favorite.save()

                return Response({"message": f"Recipe with id {recipe_id_data} added to favorites list of user with id {user_id_data}"}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Request Error'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def api_add_comment(request):
    try:
        if request.method == 'POST':
            data = request.data
            recipe_id_data = data.get('recipe_id', None)
            user_id_data = data.get('user_id', None)
            comment_text_data = data.get('comment_text', '')

            current_datetime = timezone.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d")

            if not recipe_id_data or not user_id_data or not comment_text_data:
                return Response({"message": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the recipe and user exist before adding the comment
            recipe = get_object_or_404(Recipes, pk=recipe_id_data)
            user = get_object_or_404(Users, pk=user_id_data)

            comment = Comments(recipe=recipe, user=user, comment_text=comment_text_data, comment_date=formatted_datetime)
            comment.save()

            return Response({"message": "Comment added successfully"}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Request Error'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    


@api_view(['GET'])
@csrf_exempt
def api_get_comments(request, recipe_id):
    recipe_comments = Comments.objects.order_by('-comment_date')
    serialized_comments = CommentsSerializer(recipe_comments, many=True)
    return Response({'Comments': serialized_comments.data}, status=status.HTTP_200_OK)

# --------------------- SEARCH ---------------------
# This section contains API endpoints related to search function.





