from rest_framework import viewsets
from .models import Favorites
from .serializers import FavoritesSerializer
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    @action(detail=False, methods=['GET'])
    def get_favorites_by_user_id(self, request, user_id=None):
        try:
            favorites = Favorites.objects.filter(user__id=user_id)
            serializer = self.get_serializer(favorites, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Error getting recipes by user_id"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)