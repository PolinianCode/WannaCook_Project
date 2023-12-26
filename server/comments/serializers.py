from rest_framework import serializers
from .models import Comments




class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'recipe', 'user', 'comment_text', 'comment_date']
        read_only_fields = ['comment_date']

