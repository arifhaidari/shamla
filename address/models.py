# from typing import Reversible
from django.urls import reverse
from django.db import models
# from django.core.urlresolvers import reverse
from billing.models import BillingProfile

# ADDRESS_TYPES = (
#     ('billing', 'Billing Address'),
#     ('shipping', 'Shipping Address'),
#     ('both', 'Both Address'),
# ) if it authenticated use it is name 

class Address(models.Model):
     class Types(models.TextChoices):
          Billing = 'Billing'
          Shipping = 'Shipping'
          Both = 'Both'
          
     billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True)
     full_name   = models.CharField(max_length=255, null=True, blank=True)
     company  = models.CharField(max_length=255, null=True, blank=True)
     country   = models.CharField(max_length=255, null=True, blank=True)
     city     = models.CharField(max_length=255, null=True, blank=True)
     district    = models.CharField(max_length=255, null=True, blank=True)
     street  = models.CharField(max_length=255, null=True, blank=True)
     zipcode  = models.CharField(max_length=120, null=True, blank=True)
     phone  = models.CharField(max_length=120, null=True, blank=True)
     email  = models.CharField(max_length=255, null=True, blank=True)
     apartment  = models.CharField(max_length=255, null=True, blank=True)
     address_type    = models.CharField(max_length=120, choices=Types.choices, default=Types.Both)

     def __str__(self):
          if self.city and self.country:
               return f"{self.city}, {self.country}, {self.street}"
          return "my_address"

     def get_absolute_url(self):
          return reverse("address-update", kwargs={"pk": self.pk})

     # def get_short_address(self):
     #      for_name = self.name 
     #      if self.nickname:
     #           for_name = "{} | {},".format( self.nickname, for_name)
     #      return "{for_name} {line1}, {city}".format(
     #                for_name = for_name or "",
     #                line1 = self.address_line_1,
     #                city = self.city
     #           ) 

     # def get_address(self):
     #      return "{for_name}\n{line1}\n{line2}\n{city}\n{state}, {postal}\n{country}".format(
     #                for_name = self.name or "",
     #                line1 = self.address_line_1,
     #                line2 = self.address_line_2 or "",
     #                city = self.city,
     #                state = self.state,
     #                postal= self.postal_code,
     #                country = self.country
     #           )