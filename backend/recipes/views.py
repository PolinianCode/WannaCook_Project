from rest_framework import viewsets
from .models import Recipes
from .serializers import RecipesSerializer

class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer