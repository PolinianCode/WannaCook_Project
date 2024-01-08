from rest_framework import viewsets
from .models import Categories
from .serializers import CategoriesSerializer

# Create your views here.
class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer