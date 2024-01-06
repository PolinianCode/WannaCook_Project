from django.db import models
from users.models import Users
from recipes.models import Recipes



# Comments Model (done)
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateField()

    class Meta:
        db_table = 'Comments'



