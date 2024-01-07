from rest_framework import serializers
from .models import Recipes, RecipeIngredient




class RecipeIngredientSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = RecipeIngredient
        fields = ['recipe','ingredient', 'quantity', 'unit']


class RecipesSerializer(serializers.ModelSerializer):

    ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = '__all__'
        read_only_fields = ['created_date']

