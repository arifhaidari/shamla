# Generated by Django 3.2 on 2021-10-11 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20211011_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_percentage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
