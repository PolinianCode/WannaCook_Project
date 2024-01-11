from rest_framework import viewsets
from .models import Categories
from .serializers import CategoriesSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class CategoriesViewSet(viewsets.ModelViewSet):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer