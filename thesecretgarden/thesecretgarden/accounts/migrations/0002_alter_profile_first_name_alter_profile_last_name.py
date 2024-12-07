# Generated by Django 5.1.2 on 2024-12-07 05:18

import django.core.validators
import thesecretgarden.accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=30, validators=[thesecretgarden.accounts.validators.NameValidator(field_name='first name'), django.core.validators.MinLengthValidator(3)], verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=30, validators=[thesecretgarden.accounts.validators.NameValidator(field_name='last name'), django.core.validators.MinLengthValidator(3)], verbose_name='Last Name'),
        ),
    ]
