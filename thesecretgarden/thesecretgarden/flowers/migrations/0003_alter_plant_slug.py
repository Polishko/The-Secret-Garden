# Generated by Django 5.1.2 on 2024-11-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flowers', '0002_alter_plant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='slug',
            field=models.SlugField(editable=False, unique=True, verbose_name='Slug'),
        ),
    ]
