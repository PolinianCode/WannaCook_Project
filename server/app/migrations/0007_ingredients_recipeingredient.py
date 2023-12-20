# Generated by Django 4.2.6 on 2023-12-19 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_rename_recipe_id_comments_recipe_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=20)),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ingredients')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.recipes')),
            ],
        ),
    ]