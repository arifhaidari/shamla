from django.contrib import messages
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from .utils import Mailchimp
from django.urls import reverse

from address.models import Address

User = get_user_model()


class NewsLetterType(models.Model):
     name = models.CharField(max_length=255)
     active = models.BooleanField(default=True)
     
     class Meta:
          ordering = ('-id',)
     
     def __str__(self):
          return str(self.name) or "newsletter_type_object"
     
     def get_absolute_url(self):
          return reverse('newsletter:newsletter_type_update', kwargs={'pk': self.pk})


class MailingListManager(models.Manager):
     
     def create_mailing(self, request=None, email=None, user=None, name=None):
          print('inside the create_mailing')
          the_object = None
          user_email = ''
          if user is None and request is not None:
               user = request.user if request.user.is_authenticated else None
          if name is None:
               if user is None:
                    name = email.split('@')[0]
               else:
                    name = user.full_name or email.split('@')[0]
          mailing_object = self.filter(email=email)
          if mailing_object.exists():
               the_object = mailing_object.first()
               if the_object.user is not None:
                    the_object.user = user
                    the_object.name = user.full_name
          else:
               if MailingList.objects.filter(user=user).exists():
                    user = None
               the_object = MailingList(user=user, email=email, name=name)
          if the_object is not None:
               subscription(the_object)

def subscription(the_object):
     print('inside the subscription')
     print(the_object)
     if the_object.subscribed != the_object.mailchimp_subscribed:
          print('value of instance.email in pre save')
          print(the_object.email)
          if the_object.subscribed:
               # subscribing user
               status = Mailchimp().subscribe(the_object)
          else:
               # unsubscribing user
               status = Mailchimp().unsubscribe(the_object)

          print('vlaue of status in marketing_pref_update_receiver')
          print(status)
          if status == 'subscribed':
               the_object.subscribed = True
               the_object.mailchimp_subscribed = True
          elif status == 'error':
               # leave it with default
               pass
          else:
               the_object.subscribed = False
               the_object.mailchimp_subscribed = False
     the_object.save()

class MailingList(models.Model):
     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
     name = models.CharField(max_length=255, null=True, blank=True)
     email = models.EmailField()
     active = models.BooleanField(default=True)
     subscribed = models.BooleanField(default=True)
     mailchimp_subscribed = models.BooleanField(null=True)
     updated_at = models.DateField(auto_now=True)
     created_at = models.DateTimeField(auto_now_add=True)
     
     objects = MailingListManager()
     
     class Meta:
          ordering = ('-id',)
     
     def __str__(self):
          return str(self.email) or "mailing_list_object"

@receiver(post_save, sender=User)
def create_newsletter(sender, created, instance , *args, **kwargs):
     MailingList.objects.create_mailing(user=instance, email=instance.email)

@receiver(post_save, sender=Address)
def create_newsletter(sender, created, instance , *args, **kwargs):
     user = instance.billing_profile.user or None
     MailingList.objects.create_mailing(user=user, name=instance.full_name, email=instance.email)

class NewsLetter(models.Model):
     newsletter_type = models.ForeignKey(NewsLetterType, null=True, blank=True, on_delete=models.CASCADE)
     subject = models.CharField(max_length=255, null=True, blank=True)
     greeting = models.CharField(max_length=255, null=True, blank=True)
     description = models.TextField()
     active = models.BooleanField(default=True)
     updated_at = models.DateField(auto_now=True)
     created_at = models.DateTimeField(auto_now_add=True)
     
     class Meta:
          ordering = ('-id',)
     
     def __str__(self):
          return str(self.subject) or "newsletter_object"
     
     def get_absolute_url(self):
          return reverse('newsletter:newsletter_update', kwargs={'pk': self.pk})
     
     

class CustomerMessage(models.Model):
     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
     name = models.CharField(max_length=255)
     email = models.EmailField()
     message = models.TextField()
     created_at = models.DateTimeField(auto_now_add=True)
     
     class Meta:
          ordering = ('-id',)
     
     def __str__(self):
          return self.name or "customer_message_object"


@receiver(post_save, sender=CustomerMessage)
def create_newsletter(sender, created, instance , *args, **kwargs):
     name = instance.name or instance.email.split('@')[0]
     MailingList.objects.create_mailing(user=instance.user or None, name=name, email=instance.email)



