# Generated by Django 4.2.8 on 2023-12-26 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='recipeingredient',
            table='RecipsIngredients',
        ),
        migrations.AlterModelTable(
            name='recipes',
            table='Recipes',
        ),
    ]
