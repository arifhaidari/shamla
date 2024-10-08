# Generated by Django 3.2 on 2021-11-08 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_remove_billingprofile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='default',
        ),
        migrations.RemoveField(
            model_name='card',
            name='stripe_id',
        ),
        migrations.RemoveField(
            model_name='charge',
            name='billing_profile',
        ),
        migrations.RemoveField(
            model_name='charge',
            name='outcome',
        ),
        migrations.RemoveField(
            model_name='charge',
            name='stripe_id',
        ),
        migrations.AddField(
            model_name='card',
            name='payment_intent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='card',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='billing.card'),
        ),
        migrations.AddField(
            model_name='charge',
            name='charge_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='fingerprint',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='charge',
            name='risk_score',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='risk_level',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='charge',
            name='seller_message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
