from django.conf import settings
from django.db import models
import random
from django.db.models.base import Model
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user, get_user_model
from django.dispatch import receiver

from product.models import Category

User = get_user_model()



from product.validators import image_valid_size, image_valid_type

def upload_image_path(instance, filename):
     new_filename = random.randint(1,3910209312)
     return f"sliders/{new_filename}_{filename}"

def upload_logo_path(instance, filename):
     new_filename = random.randint(1,3910209312)
     return f"logos/{new_filename}_{filename}"



class Recommendation(models.Model):
     category = models.ManyToManyField(Category, blank=True)
     item_number = models.IntegerField(default=0)
     
     def __str__(self):
          return str(self.item_number) or 'Unknown Object'

class NewArrival(models.Model):
     time_interval = models.DateField(null=True, blank=True)
     item_number = models.IntegerField(default=0)
     
     def __str__(self):
          return str(self.time_interval) or 'Unnknown Object'

class Slider(models.Model):
     title = models.CharField(max_length=25)
     subtitle = models.CharField(max_length=25)
     active = models.BooleanField(default=True)
     image = models.ImageField(
          upload_to=upload_image_path, null=True, blank=True, validators=[image_valid_size, image_valid_type]
          )
     
     def __str__(self):
          return self.title or self.subtitle

class Brand(models.Model):
     name = models.CharField(max_length=200)
     web = models.CharField(max_length=255, null=True, blank=True)
     active = models.BooleanField(default=True)
     logo = models.ImageField(
          upload_to=upload_logo_path, null=True, blank=True, validators=[image_valid_size, image_valid_type]
          )
     
     def __str__(self):
          return self.name or self.web


class CoolCustomerDiscount(models.Model):
     trigger_amount = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
     discount_by_amount = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
     discount_by_percentage = models.IntegerField(null=True, blank=True)
     active = models.BooleanField(default=False)
     
     def __str__(self):
          return self.trigger_amount or ''


class SpecialOffer(models.Model):
     event = models.CharField(max_length=255)
     discount_by_percentage = models.IntegerField(null=True, blank=True)
     active = models.BooleanField(default=False)
     
     def __str__(self):
          return self.event or ""





