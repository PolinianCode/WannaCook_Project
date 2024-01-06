from django.db import models
from users.models import Users
from recipes.models import Recipes

# Rating Model (done)
class Ratings(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    value = models.IntegerField()


    class Meta:
        db_table = 'Ratings'