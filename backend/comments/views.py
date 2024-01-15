from rest_framework import viewsets
from .models import Comments
from .serializers import CommentsSerializer
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import action

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def list(self, request):
        queryset = Comments.objects.filter(recipe_id=request.query_params.get('recipe_id')).order_by('-comment_date')
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data)






