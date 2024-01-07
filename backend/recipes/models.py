from django.db import models
from django.contrib.auth.models import User
from categories.models import Categories
# Create your models here.
class Recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField() 
    instruction = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    rating_sum = models.IntegerField()
    rating_num = models.IntegerField()


    class Meta:
        db_table = 'Recipes'