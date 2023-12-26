from rest_framework import serializers
from .models import Recipes, RecipeIngredient


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'
        read_only_fields = ['created_date']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ['recipe','ingredient', 'quantity', 'unit']
