from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer



@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'Message': 'Email is already exists'}, status=400)

        user = User.objects.create_user(username=username, password = password, email=email)

        if user:

           

            login(request, user)
            return JsonResponse({'Message': 'User has been created'}, status=200)
        else:
            return JsonResponse({'Message': 'Error while creating user'}, status=400)
    return JsonResponse({'message': 'Invalid request method'}, status=405) 




@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            user_serialized = UserSerializer(user)
            print(request.session.items())
            return JsonResponse({
                'message': 'Login successful',
                'user': user_serialized.data,
            }, status=200)
        else:
            return JsonResponse({'Message': 'Invalid login credentials'}, status=401)

    return JsonResponse({'message': 'Invalid request method'}, status=405)  


@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({'Message': 'Logout successfull'}, status=200)
