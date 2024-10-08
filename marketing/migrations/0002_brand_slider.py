# Generated by Django 3.2 on 2021-10-09 09:15

import django.core.validators
from django.db import migrations, models
import marketing.models
import product.validators


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('web', models.CharField(blank=True, max_length=255, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=marketing.models.upload_logo_path, validators=[product.validators.image_valid_size, django.core.validators.FileExtensionValidator()])),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('subtitle', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to=marketing.models.upload_image_path, validators=[product.validators.image_valid_size, django.core.validators.FileExtensionValidator()])),
            ],
        ),
    ]
