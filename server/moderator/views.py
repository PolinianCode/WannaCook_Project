from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import Users

# --------------------- Moderator ---------------------
    
@api_view(['PUT'])
@csrf_exempt
def api_set_moderator(request):
    try:
        user_id = request.data.get("user_id")
        user_status = request.data.get("status")

        if user_id is None:
            return Response({"error": "Missing user id"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(Users, user_id=user_id)

        user.is_moderator = user_status 

        user.save()

        if user_status:
            return Response({"message": f"User {user_id} upgraded to moderator"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": f"User {user_id} downgraded to user"}, status=status.HTTP_200_OK)

    except Users.DoesNotExist:
        return Response({"error": f"User with ID {user_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)

