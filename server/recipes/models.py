from django.db import models
from users.models import Users
from categories.models import Categories
from ingredient.models import Ingredients

class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField() 
    instruction = models.TextField()
    created_date = models.DateField()
    rating_sum = models.IntegerField()
    rating_num = models.IntegerField()


    class Meta:
        db_table = 'Recipes'

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=20)

    class Meta:
        db_table = 'RecipsIngredients'