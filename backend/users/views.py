from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import authentication_classes
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
#improt status
from rest_framework import status
#import api 
from rest_framework.decorators import api_view



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
            if Token.objects.filter(user=user).exists():
                token = Token.objects.get(user=user)
                token.delete()
            token = Token.objects.create(user=user)
            user_serialized = UserSerializer(user)
            login(request, user)
            return JsonResponse({
                'message': 'User has been created',
                'user': user_serialized.data,
                'token': token.key
            }, status=200)
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
            if Token.objects.filter(user=user).exists():
                token = Token.objects.get(user=user).delete()
            token = Token.objects.create(user=user)
            print(token.key)
            login(request, user)
            user_serialized = UserSerializer(user)
            print(request.session.items())
            return JsonResponse({
                'message': 'Login successful',
                'user': user_serialized.data,
                'token': token.key
            }, status=200)
        else:
            return JsonResponse({'Message': 'Invalid login credentials'}, status=401)

    return JsonResponse({'message': 'Invalid request method'}, status=405)  


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def logout_user(request):
    Token.objects.get(user=request.user).delete()
    logout(request)
    return JsonResponse({'Message': 'Logout successfull'}, status=200)


@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def token_check(request):
    return Response({'Message': 'Token is valid'}, status=status.HTTP_200_OK)
    # if request.method == 'POST':
    #     token = request.get('token')
    #     if Token.objects.filter(key=token).exists():
    #         return JsonResponse({'Message': 'Token is valid'}, status=200)
    #     else:
    #         return JsonResponse({'Message': 'Token is invalid'}, status=400)
    # return JsonResponse({'Message': 'Invalid request method'}, status=405)
