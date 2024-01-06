from .models import Users
from rest_framework import serializers


class UsersWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'nickname', 'email', 'password', 'is_moderator', 'registration_date']
        read_only_fields = ['registration_date']

class UsersReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ['password']