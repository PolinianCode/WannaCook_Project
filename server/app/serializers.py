from rest_framework import serializers
from .models import Users, Comments, Categories, Recipes, Favorites, Ingredients


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'nickname', 'email', 'is_moderator', 'registration_date']
        read_only_fields = ['registration_date']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'recipe', 'user', 'comment_text', 'comment_date']
        read_only_fields = ['comment_date']



class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'
        read_only_fields = ['created_date']


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'