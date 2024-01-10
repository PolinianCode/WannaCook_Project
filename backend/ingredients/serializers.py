from rest_framework import serializers
from .models import Ingredients, RecipeIngredient

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'