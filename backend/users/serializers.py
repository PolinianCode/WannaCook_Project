from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


#user serializers without sensitive data
class UserSerializerWithoutSensitiveData(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']