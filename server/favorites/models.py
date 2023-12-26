from django.db import models
from users.models import Users
from recipes.models import Recipes

# Favorites Model (done)
class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Favorites'
