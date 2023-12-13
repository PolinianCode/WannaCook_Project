from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from django.http import HttpResponse
from django.utils import timezone
from .models import Recipes
from .models import Users
from .models import Categories
import json
from .utils import check_user_exist, check_user_email_exist
from django.shortcuts import get_object_or_404


#Get all users from DB
@csrf_exempt
def api_get_users(request):
    all_users = Users.objects.order_by('-user_id')[:5]
    serialized_users = serialize('json', all_users)
    return JsonResponse({'latest_recipes':  serialized_users}, safe=False)

#Add new user do db
@csrf_exempt
def api_add_user(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            nickname_data = data.get('nickname', '')
            email_data = data.get('email', '')
            password_data = data.get('password', '')
            is_moderator_data = data.get('is_moderator', '0')

            current_datetime = timezone.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d")

            if not nickname_data or not email_data or not password_data:
                return JsonResponse({'error': 'Missing parameters!'}, status=400)

            if check_user_exist(nickname_data) or check_user_email_exist(email_data):
                return JsonResponse({'error': 'User exists!'}, status=400)
            else:
                user = Users(nickname=nickname_data, email=email_data, password=password_data, registration_date=formatted_datetime, is_moderator=is_moderator_data)
                user.save()

                return JsonResponse({'message': 'User has been created!'})
        else:
            return JsonResponse({'error': 'Request Error'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    
#Remove user with nickname
@csrf_exempt
def api_remove_user(request, username):
    try:
        user = get_object_or_404(Users, nickname=username)

        user.delete()

        return JsonResponse({"message": f"User {username} has been deleted."})
    except Exception as e:
        print(e)
        return JsonResponse({"message": f"User {username} doesn't exist"})
    

#Add new Recipe to DB
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
                return JsonResponse({"message": f"Missing user id"})

            if not title_data or not description_data or not instructions_data or not category_name_data:
                return JsonResponse({"message": f"Missing required parameters"})
            
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

            return JsonResponse({"message": f"The recipe has been added successfully"})
        
        else:
            return JsonResponse({'error': 'Request Error'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({"message": f"Recipe cant be added to DB {e}"})


#Get all recipe categories from DB
@csrf_exempt
def api_load_recipe_categories(request):
    all_categories = Categories.objects.order_by('-id')
    serialized_categories = serialize('json', all_categories)
    return JsonResponse({'all_categories':  serialized_categories}, safe=False)

@csrf_exempt
def api_modify_recipe(request, recipe_id):

    try:
        recipe = get_object_or_404(Recipes, pk=recipe_id)

        if request.method == "PUT" or request.method == "PATCH":
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

            return JsonResponse({"message": f"The recipe has been modified successfully"})
        else:
            return JsonResponse({'error': 'Invalid Request Method'}, status=400)

    except Exception as e:
        print(e)
        return JsonResponse({"message": f"Recipe modification failed: {e}"})
    

def api_delete_recipe(request, recipe_id):
     try:
        recipe = get_object_or_404(Recipes, recipe_id=recipe_id)

        recipe.delete()

        return JsonResponse({"message": f"Recipe {recipe_id} has been deleted."})
     except Exception as e:
        print(e)
        return JsonResponse({"message": f"Recipe {recipe_id} doesn't exist"})
         
  
    