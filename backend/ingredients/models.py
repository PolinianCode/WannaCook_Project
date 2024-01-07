from django.db import models
from recipes.models import Recipes

# Create your models here.
class Ingredients(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Ingredients'

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)

    class Meta:
        db_table = 'RecipsIngredients'