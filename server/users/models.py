from django.db import models

# User Model (done)
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    registration_date = models.DateField()
    is_moderator = models.BooleanField()

    class Meta:
        db_table = 'Users'
