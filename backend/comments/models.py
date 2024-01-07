from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipes

# Create your models here.
class Comments(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Comments'