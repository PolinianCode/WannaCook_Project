from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Comments
from .serializers import CommentsSerializer

# --------------------- Comments ---------------------
# Add comment to recipe
@api_view(['POST'])
@csrf_exempt
def api_add_comment(request):
    try:

        current_datetime = timezone.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d")

        serializer = CommentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['comment_date'] = formatted_datetime
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment couldn't be added: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Remove comment from recipe
@api_view(['DELETE'])
@csrf_exempt
def api_remove_comment(request):
    try:
        comment_id = request.data.get("comment_id")

        comment = get_object_or_404(Comments, pk=comment_id)
        comment.delete()

        return Response({"message": f"Comment {comment_id} has been deleted."}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        print(e)
        return Response({"message": f"Comment {comment_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)


# Edit comment 
@api_view(['PUT'])
@csrf_exempt
def api_modify_comment(request):
    try:
        comment_id = request.data.get("comment_id")  

        if comment_id is None:
            return Response({"message": "Comment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = get_object_or_404(Comments, pk=comment_id)

        data = request.data
        comment_text_data = data.get('comment_text', comment.comment_text)

        comment.comment_text = comment_text_data
        comment.save()

        return Response({"message": f"Comment {comment_id} has been modified successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": f"Comment modification failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get comments for recipe
@api_view(['GET'])
@csrf_exempt
def api_get_comments(request):
    try:
        recipe_id = request.data.get('recipe_id')
        comments = Comments.objects.filter(recipe=recipe_id).order_by('-id')
        serialized_comments = CommentsSerializer(comments, many=True)
        return Response({'Comments': serialized_comments.data}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



