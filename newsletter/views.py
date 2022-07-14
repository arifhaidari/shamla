from re import template
from typing import List
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, ListView, DetailView, UpdateView

from newsletter.models import CustomerMessage, MailingList, NewsLetter, NewsLetterType
from shamla.utils import empty_none_validator
from django.core.mail import send_mass_mail
from django.conf import settings


class MailingListView(ListView):
     template_name = 'newsletter/admin/mailing_list.html'
     model = MailingList

class NewsletterTypeView(ListView):
     template_name = 'newsletter/admin/newsletter_type_list.html'
     model = NewsLetterType


# Create
class NewsletterTypeCreateView(View):
     template_name = 'newsletter/admin/newsletter_type_create.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               name = request.POST.get('name', None)
               check_box = request.POST.get('is_active', None)
               if name is None or name == '':
                    messages.error(self.request, "Newsletter type field is empty")
               else:
                    is_checked = check_box is not None
                    NewsLetterType.objects.create(name=name, active=is_checked)
                    messages.success(self.request, "Newsletter type is saved successfully!")
          return render(request, self.template_name, {})


# Update
class NewsletterTypeUpdateView(UpdateView):
     template_name = 'newsletter/admin/newsletter_type_update.html'
     model = NewsLetterType
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               name = request.POST.get('name', None)
               check_box = request.POST.get('is_active', None)
               if name is None or name == '':
                    messages.error(self.request, "Newsletter type field is empty")
               else:
                    try:
                         obj = self.get_object()
                         obj.name = name
                         obj.active = check_box is not None
                         obj.save()
                         return redirect('newsletter:newsletter_type_list')
                    except:
                         pass
          return render(request, self.template_name, {'object': self.get_object()})


class NewsletterView(ListView):
     template_name = 'newsletter/admin/newsletter_list.html'
     model = NewsLetter


# Create
class NewsletterCreateView(View):
     template_name = 'newsletter/admin/newsletter_create.html'
     
     def the_data(self):
          data = {
               'types': NewsLetterType.objects.filter(active=True)
          }
          return data
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, self.the_data())
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               newsletter_type = request.POST.get('newsletter_type', None)
               subject = request.POST.get('subject', None)
               greeting = request.POST.get('greeting', None)
               description = request.POST.get('description', None)
               is_valid = empty_none_validator([subject, description, greeting])
               if not is_valid:
                    messages.error(self.request, "Newsletter required fields i.e. subject, greeting or description are empty")
               else:
                    try:
                         newsletter_type = newsletter_type if empty_none_validator([newsletter_type, ]) and newsletter_type != 'all' else None
                         if newsletter_type is not None:
                              try:
                                   newsletter_type = NewsLetterType.objects.get(id=newsletter_type)
                              except:
                                   newsletter_type = None
                         NewsLetter.objects.create(
                              newsletter_type=newsletter_type, subject=subject, 
                              description=description, greeting=greeting
                              )
                         # send email from here
                         mailing_list = MailingList.objects.filter(subscribed=True).exclude(email='arifmoazy351@gmail.com')
                         list_tuple = []
                         for mail in mailing_list:
                              the_body = f'{greeting} {mail.name};' + '\n' + description
                              list_tuple.append((subject, the_body, settings.DEFAULT_FROM_EMAIL, [mail.email]))
                         datatuple = tuple(list_tuple)
                         if len(datatuple) != 0:
                              send_mass_mail(datatuple)
                         messages.success(self.request, "Newsletter is saved and sent successfully!")
                    except Exception as e:
                         print('some error occurd')
                         print(e)
                         messages.error(self.request, "Uknown error occured. Please try again")
                         
          return render(request, self.template_name, self.the_data())


# Update
class NewsletterUpdateView(UpdateView):
     template_name = 'newsletter/admin/newsletter_update.html'
     model = NewsLetter
     
     def the_data(self):
          data = {
               'types': NewsLetter.objects.filter(active=True),
               'object': self.get_object()
          }
          return data
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, self.the_data())

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               newsletter_type = request.POST.get('newsletter_type', None)
               subject = request.POST.get('subject', None)
               greeting = request.POST.get('greeting', None)
               description = request.POST.get('description', None)
               is_valid = empty_none_validator([subject, description])
               if not is_valid:
                    messages.error(self.request, "Newsletter required fields i.e. subject, greeting or description are empty")
               else:
                    try:
                         newsletter_type = newsletter_type if empty_none_validator([newsletter_type, ]) and newsletter_type != 'all' else None
                         if newsletter_type is not None:
                              try:
                                   newsletter_type = NewsLetterType.objects.get(id=newsletter_type)
                              except:
                                   newsletter_type = None
                         # update
                         newsletter_obj = self.get_object()
                         newsletter_obj.newsletter_type = newsletter_type
                         newsletter_obj.subject = subject
                         newsletter_obj.greeting = greeting
                         newsletter_obj.description = description
                         newsletter_obj.save()
                         # send email from here
                         mailing_list = MailingList.objects.filter(subscribed=True).exclude(email='arifmoazy351@gmail.com')
                         list_tuple = []
                         for mail in mailing_list:
                              the_body = f'{greeting} {mail.name};' + '\n' + description
                              list_tuple.append((subject, the_body, settings.DEFAULT_FROM_EMAIL, [mail.email]))
                         datatuple = tuple(list_tuple)
                         if len(datatuple) != 0:
                              send_mass_mail(datatuple)
                         messages.success(self.request, "Newsletter is saved and sent successfully!")
                    except:
                         pass
          return render(request, self.template_name, self.the_data())


class CustomerMessageListView(ListView):
     template_name = 'newsletter/admin/customer_message_list.html'
     model = CustomerMessage
