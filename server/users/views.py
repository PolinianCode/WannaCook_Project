from urllib.parse import unquote_plus
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponse
from .models import Users
from .serializers import UsersReadSerializer, UsersWriteSerializer
from .utils import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout


# --------------------- USER ---------------------
# This section contains API endpoints related to user operations.


# Get all users from database.
@api_view(['GET'])
@csrf_exempt
def api_get_users(request):
    all_users = Users.objects.order_by('-user_id')
    serialized_users = UsersReadSerializer(all_users, many=True)
    return Response({'users': serialized_users.data}, status=status.HTTP_200_OK)


# Add a new user to the database.
@api_view(['POST'])
@csrf_exempt
def api_register_user(request):
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
        

        serializer = UsersWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['registration_date'] = formatted_datetime
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User has been created!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Get user data (LOGIN)
@api_view(['GET'])
@csrf_exempt
def api_login_user(request):
    encoded_data = request.GET.get('data', '')
    decoded_data = unquote_plus(encoded_data)

    data = json.loads(decoded_data)

    username = data.get('nickname')
    password = data.get('password')

    print(f"Received credentials - Username: {username}, Password: {password}")

    if not username or not password:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = Users.objects.filter(nickname=username, password=password).first()

    #user = authenticate(request, nickname=username, password=password)

    print(f"Authentication result: {user}")


    if user is not None:
        #login(request, user)
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
        return Response({"message": f"User {username} has been deleted."}, status=status.HTTP_200_OK)
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


@csrf_exempt
@api_view(['POST'])
def api_get_user(request):
    id = request.data.get('user_id')

    user = Users.objects.get(user_id = id)
    serializedUser = UsersReadSerializer(user, many=False)
    return Response({'User': serializedUser.data}, status=status.HTTP_200_OK)
