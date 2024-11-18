# Generated by Django 5.1.2 on 2024-11-18 16:52

import django.core.validators
import thesecretgarden.gifts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(help_text='Enter the brand name.', max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Brand Name')),
                ('short_name', models.CharField(help_text='Enter the product short name.', max_length=50, unique=True, verbose_name='Short Name')),
                ('short_description', models.CharField(help_text='Enter short product description.', max_length=100, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Short Description')),
                ('slug', models.SlugField(editable=False, unique=True)),
                ('type', models.CharField(choices=[('red wine', 'Red Vine'), ('chocolate', 'Chocolate'), ('candle', 'Candle')], help_text='Provide gift type.', max_length=9, verbose_name='Type')),
                ('price', models.DecimalField(decimal_places=2, help_text='Provide gift price.', max_digits=7, validators=[thesecretgarden.gifts.validators.GiftPriceValidator()], verbose_name='Price')),
                ('stock', models.PositiveIntegerField(help_text='Provide stock amount.', verbose_name='Stock')),
                ('photo', models.ImageField(upload_to='images/gifts', validators=[thesecretgarden.gifts.validators.FileSizeValidator(5)])),
            ],
            options={
                'verbose_name': 'Gift',
                'ordering': ['brand_name'],
            },
        ),
    ]
