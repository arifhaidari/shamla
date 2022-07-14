from decimal import Decimal
from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.db.models import Sum
from product.models import Product, Size, Color
from django.dispatch import receiver


User = get_user_model()

class CartManager(models.Manager):
     def new_or_get(self, request, the_cart_id=None, the_user=None):
          print('inside the new_or_get')
          print(the_cart_id, the_user, request.user)
          cart_id = request.session.get("cart_id", None)
          print('value fo cart_id')
          print(cart_id)
          user = request.user
          if the_user is not None:
               user = the_user
          if the_cart_id is not None:
               cart_id = the_cart_id
          qs = self.get_queryset().filter(id=cart_id, is_checked_out=False)
          if qs.count() != 0 and cart_id is not None:
               new_obj = False
               cart_obj = qs.first()
               if user.is_authenticated and cart_obj.user is None:
                    cart_obj.user = user
                    cart_obj.save()
          else:
               print('new cart is crated')
               cart_obj = Cart.objects.new(user=user, unvalid_user=the_user)
               new_obj = True
               request.session['cart_id'] = cart_obj.id
          return cart_obj, new_obj
     
     def new(self, user=None, unvalid_user=None):
          user_obj = None
          if user is not None:
               if user.is_authenticated:
                    user_obj = user
               else:
                    if unvalid_user is not None:
                         user_obj = unvalid_user
          return self.model.objects.create(user=user_obj)


class Cart(models.Model):
     user  = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
     shipment_fee = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
     is_checked_out = models.BooleanField(default=False)
     updated_at     = models.DateTimeField(auto_now=True)
     timestamp   = models.DateTimeField(auto_now_add=True)

     objects = CartManager()

     def __str__(self):
          return str(self.timestamp)
     
     @property
     def current_item_num(self):
          if len(self.cartproduct_set.all()) != 0:
               total = self.cartproduct_set.aggregate(Sum('product_quantity'))
               return total['product_quantity__sum'] or 0
          return 0
     
     @property
     def purchase_price_total(self):
          result = 0
          if len(self.cartproduct_set.all()) != 0:
               for item in self.cartproduct_set.all():
                    result += item.total_purchase_price
          return result
     
     @property
     def subtotal(self):
          result = 0
          if len(self.cartproduct_set.all()) != 0:
               for item in self.cartproduct_set.all():
                    result += item.subtotal_price
          return result
     
     @property
     def total(self):
          result = 0
          if len(self.cartproduct_set.all()) != 0:
               for item in self.cartproduct_set.all():
                    result += item.total_price
          return (result - self.shipment_fee) or 0.00
     
     @property
     def discount_total(self):
          result = 0
          if len(self.cartproduct_set.all()) != 0:
               for item in self.cartproduct_set.all():
                    result += item.total_discount
          return result
     
class CartProduct(models.Model):
     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.CASCADE)
     color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
     product_quantity = models.IntegerField(default=0)
     product_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
     product_purchase_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
     product_discount = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
     
     def __str__(self):
          return str(self.cart.timestamp) or ""
     
     @property
     def total_purchase_price(self):
          if self.product_purchase_price is not None and self.product_purchase_price != 0 and self.product_quantity is not None and self.product_quantity != 0:
               return (self.product_quantity * self.product_purchase_price) or 0
          return 0
     
     @property
     def total_discount(self):
          if self.product_discount is not None and self.product_discount != 0 and self.product_quantity is not None and self.product_quantity != 0:
               return (self.product_quantity * self.product_discount) or 0
          return 0
     
     @property
     def total_price(self):
          if (self.product_quantity is not None and self.product_quantity != 0 and 
              self.product_price is not None and self.product_price != 0 and self.product_discount is not None):
               return ((self.product_quantity * self.product_price) - (self.product_quantity * self.product_discount)) or 0
          return 0
     
     @property
     def subtotal_price(self):
          if (
               self.product_quantity is not None and self.product_quantity != 0 
               and self.product_price is not None and self.product_price != 0):
               return (self.product_quantity * self.product_price) or 0
          return 0
         

class WishList(models.Model):
     user  = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
     updated_at     = models.DateTimeField(auto_now=True)
     timestamp   = models.DateTimeField(auto_now_add=True)

     objects = CartManager()

     def __str__(self):
          return str(self.timestamp)

class WishListItem(models.Model):
     wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.CASCADE)
     color = models.ForeignKey(Color, null=True, blank=True, on_delete=models.CASCADE)
     
     def __str__(self):
          return str(self.wishlist) or "wish_list_item_object"

@receiver(post_save, sender=User)
def create_wihlist(sender, instance, created, *args, **kwargs):
     if not WishList.objects.filter(user=instance).exists():
          WishList.objects.create(user=instance)




