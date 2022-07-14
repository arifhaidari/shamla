from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from account.models import GuestEmail
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

# abc@teamcfe.com -->> 1000000 billing profiles
# user abc@teamcfe.com -- 1 billing profile

import stripe
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_kelVPmtJ1IDnXDF3oaQGq4JL000WOFQ3tY")
stripe.api_key = STRIPE_SECRET_KEY


class BillingProfileManager(models.Manager):
     def new_or_get(self, request):
          user = request.user
          created = False
          obj = None
          if user.is_authenticated:
               'logged in user checkout; remember payment stuff'
               obj, created = self.model.objects.get_or_create(
                              user=user)
          else:
               pass
          return obj, created


class BillingProfile(models.Model):
     user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
     active      = models.BooleanField(default=True)
     update      = models.DateTimeField(auto_now=True)
     timestamp   = models.DateTimeField(auto_now_add=True)
     customer_id = models.CharField(max_length=120, null=True, blank=True)
     # customer_id in Stripe or Braintree

     objects = BillingProfileManager()

     def __str__(self):
          return self.user.full_name or "the_object"
     

@receiver(pre_save, sender=BillingProfile)
def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    if not instance.customer_id and instance.user.email:
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(
                email = instance.user.email
            )
        print(customer)
        instance.customer_id = customer.id


@receiver(post_save, sender=User)
def user_created_receiver(sender, instance, created, *args, **kwargs):
     if created and instance.email:
          BillingProfile.objects.get_or_create(user=instance)



class Card(models.Model):
     billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
     payment_intent          = models.CharField(max_length=255, null=True, blank=True) 
     brand                   = models.CharField(max_length=120, null=True, blank=True) # network
     country                 = models.CharField(max_length=50, null=True, blank=True)
     exp_month               = models.IntegerField(null=True, blank=True)
     exp_year                = models.IntegerField(null=True, blank=True)
     last4                   = models.CharField(max_length=4, null=True, blank=True)
     active                  = models.BooleanField(default=True)
     timestamp               = models.DateTimeField(auto_now_add=True)


     def __str__(self):
          return "{} {}".format(self.brand, self.last4)


class Charge(models.Model):
     card         = models.ForeignKey(Card, on_delete=models.CASCADE, null=True, blank=True)
     charge_id               = models.CharField(max_length=255, null=True, blank=True) 
     fingerprint             = models.CharField(max_length=255, null=True, blank=True) 
     paid                    = models.BooleanField(default=False)
     refunded                = models.BooleanField(default=False)
     outcome_type            = models.CharField(max_length=120, null=True, blank=True)
     seller_message          = models.CharField(max_length=255, null=True, blank=True)
     risk_level              = models.CharField(max_length=80, null=True, blank=True)
     risk_score              = models.CharField(max_length=80, null=True, blank=True)
     
     def __str__(self):
          return self.charge_id or "charge_id"



