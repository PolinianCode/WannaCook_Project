from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt(['POST'])
def userLogin(request):
