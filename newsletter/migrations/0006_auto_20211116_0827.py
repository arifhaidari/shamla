# Generated by Django 3.2 on 2021-11-16 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsletter', '0005_alter_mailinglist_mailchimp_subscribed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailinglist',
            name='mailchimp_msg',
        ),
        migrations.AddField(
            model_name='customermessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
