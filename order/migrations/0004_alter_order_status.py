# Generated by Django 3.2 on 2021-11-02 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20211016_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Created', 'Created'), ('Paid', 'Paid'), ('Shipped', 'Shipped'), ('Refunded', 'Refunded')], default='Created', max_length=120),
        ),
    ]
