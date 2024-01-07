from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipes

# Create your models here.
class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    value = models.IntegerField()


    class Meta:
        db_table = 'Ratings'