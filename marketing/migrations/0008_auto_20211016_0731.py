# Generated by Django 3.2 on 2021-10-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_discount_percentage'),
        ('marketing', '0007_newarrival_recommendation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='category',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='category',
            field=models.ManyToManyField(to='product.Category'),
        ),
    ]
