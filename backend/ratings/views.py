from rest_framework import viewsets
from .models import Ratings
from .serializers import RatingsSerializer

class RatingsViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingsSerializer