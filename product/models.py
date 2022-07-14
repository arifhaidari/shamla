import random
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.db import models
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.signals import post_delete, pre_save, post_save
from django.urls import reverse
from product.validators import image_valid_size, image_valid_type
from django.dispatch import receiver

# from ecommerce.aws.download.utils import AWSDownload
# from ecommerce.aws.utils import ProtectedS3Storage
from shamla.utils import unique_slug_generator, get_filename

def get_filename_ext(filepath):
     base_name = os.path.basename(filepath)
     name, ext = os.path.splitext(base_name)
     return name, ext


def upload_image_path(instance, filename):
     # print(instance)
     #print(filename)
     new_filename = random.randint(1,3910209312)
     # name, ext = get_filename_ext(filename)
     # final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
     return f"products/{new_filename}_{filename}"

class Color(models.Model):
     name = models.CharField(max_length=255)
     active      = models.BooleanField(default=True)
     
     def __str__(self):
          return self.name or ""


class Size(models.Model):
     name = models.CharField(max_length=255)
     active      = models.BooleanField(default=True)
     
     def __str__(self):
          return self.name or ""


class Category(models.Model):
     name = models.CharField(max_length=255)
     active = models.BooleanField(default=True)
     
     def __str__(self):
          return self.name or ""
     
     
class Tag(models.Model):
     name = models.CharField(max_length=255)
     active = models.BooleanField(default=True)
     
     def __str__(self):
          return self.name or ""


class ProductQuerySet(models.query.QuerySet):
     def active(self):
          return self.filter(active=True)

     def search(self, query):
          lookups = (Q(title__icontains=query) | 
                    Q(description__icontains=query) |
                    Q(price__icontains=query) |
                    Q(tag__title__icontains=query)
                    )
          # tshirt, t-shirt, t shirt, red, green, blue,
          return self.filter(lookups).distinct()

class ProductManager(models.Manager):
     def get_queryset(self):
          return ProductQuerySet(self.model, using=self._db)

     def all(self):
          return self.get_queryset().active()

     def get_by_id(self, id):
          qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
          if qs.count() == 1:
               return qs.first()
          return None

     def search(self, query):
          return self.get_queryset().active().search(query)

class Product(models.Model):
     title           = models.CharField(max_length=255)
     product_code    = models.CharField(max_length=255, null=True, blank=True)
     slug            = models.SlugField(blank=True, unique=True)
     description     = models.TextField()
     price           = models.DecimalField(decimal_places=2, max_digits=20)
     old_price       = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
     discount_percentage  = models.IntegerField(null=True, blank=True)
     purchase_price  = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
     stock           = models.IntegerField(default=0)
     size            = models.ManyToManyField(Size, blank=True)
     color           = models.ManyToManyField(Color, blank=True)
     category        = models.ManyToManyField(Category, blank=True)
     tag             = models.ManyToManyField(Tag, blank=True)
     active          = models.BooleanField(default=True)
     timestamp       = models.DateTimeField(auto_now_add=True)
     updated         = models.DateTimeField(auto_now=True)

     objects = ProductManager()

     def get_absolute_url(self):
          return reverse("product:product_detail", kwargs={"slug": self.slug})
     
     def get_absolute_url_admin(self):
          return reverse("product:admin_product_detail", kwargs={"slug": self.slug})

     def __str__(self):
          return self.title
     
     @property
     def discount_amount(self):
          if self.discount_percentage is not None and self.discount_percentage != 0:
               return (self.price * self.discount_percentage) / 100
          return 0

     @property
     def name(self):
          return self.title


class ProductImages(models.Model):
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     image = models.ImageField(
          upload_to=upload_image_path, null=True, blank=True, validators=[image_valid_size, image_valid_type]
          )
     
     def __str__(self):
          return self.product.title or ""
     
     # def delete(self, *args, **kwargs):
     #      print('delte the image ------')
     #      self.image.delete()
     #      super().delete(*args, **kwargs)

@receiver(post_delete, sender=ProductImages)
def post_delete_image(sender, instance, *args, **kwargs):
     """ Clean Old Image file """
     try:
          print('it is dlete dude =====')
          instance.image.delete(save=False)
     except:
          pass
   
def product_pre_save_receiver(sender, instance, *args, **kwargs):
     if not instance.slug:
          instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)









