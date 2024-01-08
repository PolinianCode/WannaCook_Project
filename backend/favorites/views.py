from rest_framework import viewsets
from .models import Favorites
from .serializers import FavoritesSerializer

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer