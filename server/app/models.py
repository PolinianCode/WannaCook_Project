from django.db import models


# Categories model (done)
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    

# User Model (done)
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    registration_date = models.DateField()
    is_moderator = models.BooleanField()

# Recipes Model (done)
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

class Ingredients(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20)

# Rating Model (done)
class Ratings(models.Model):
    user = models.ForeignKey(Users, primary_key=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    value = models.IntegerField()

# Comments Model (done)
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateField()

# Rating Model (done)
class Ratings(models.Model):
    user = models.ForeignKey(Users, primary_key=True, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    value = models.IntegerField()



# Favorites Model (done)
class Favorites(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)


