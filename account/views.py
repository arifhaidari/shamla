from django.db import models
from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View, ListView, DetailView
from django.contrib.auth import  authenticate, get_user_model, login
from django.views.generic.base import TemplateResponseMixin
from address.models import Address
from order.models import Order
from shamla.views import get_cart_brief_items
# from django.views.generic.base import TemplateView

User = get_user_model()



class UserProfile(View):
     template_name = 'account/profile.html'

     def profile_data(self, user):
          dashboard_context = {
               'orders': Order.objects.filter(billing_profile__user=user).order_by('-id'),
               'addresses': Address.objects.filter(billing_profile__user=user).order_by('-id'),
               'cart_data': get_cart_brief_items(self.request),
          }
          return dashboard_context

     def get(self, request, *args, **kwargs):
          user = request.user
          if user.admin:
               return render(request, 'account/admin/admin_dashboard.html', {})
          # normal user data
          dashboard_context = self.profile_data(user)
          return render(request, self.template_name, dashboard_context)

     def post(self, request, *args, **kwargs):
          user = request.user
          dashboard_context = self.profile_data(user)
          if request.method == 'POST':
               print('value of post')
               print(request.POST)
               email = request.POST.get('email', None)
               full_name = request.POST.get('full_name', None)
               current_pass = request.POST.get('current_pass', None)
               new_pass = request.POST.get('new_pass', None)
               confirm_pass = request.POST.get('confirm_pass', None)
               is_error = (current_pass == '' or new_pass == '' or confirm_pass == ''
                           or new_pass != confirm_pass or full_name == '' or email == '')
               if not is_error:
                    print('error is in field')
                    try:
                         user = User.objects.get(email=email)
                         if user.check_password(current_pass):
                              user.full_name = full_name
                              user.set_password(new_pass)
                              user.save()
                              authenticated_user = authenticate(request, username=email, password=new_pass)
                              login(request, authenticated_user)
                         else:
                              print('password does not match')
                              is_error = True
                    except:
                         is_error = True
               if is_error:
                    messages.error(request, 'Oops Error. Fill inputs properly and try again')
               else:
                    messages.success(request, 'User info is updated successfully')
          return render(request, self.template_name, dashboard_context)


class RegisterView(View):
     template_name = "account/register.html"

     def get(self, request, *args, **kwargs):
          if self.request.user.is_authenticated:
               return redirect("home")
          return render(request, self.template_name, {})

     def post(self, request, *args, **kwargs):
          if request.method == "POST":
               print('value of post ======')
               print(request.POST)
               fullname = request.POST.get("full_name")
               email = request.POST.get("email")
               password = request.POST.get("password")
               newsletter = request.POST.get("newsletter")
               is_form_correct = (fullname is None or 
                                  email is None or password is None)
               if is_form_correct:
                    messages.error(self.request, "Please enter your data correctly")
                    return render(request, self.template_name, {})
               if self.request.user.is_authenticated:
                    messages.error(self.request, "There is a user already signed in. Login instead")
                    return render(request, self.template_name, {})
               is_email = User.objects.filter(email=email)
               if is_email.exists():
                    messages.error(
                    request,
                    "Email is already existed in the system",
                    )
                    return render(request, self.template_name, {})
               User.objects.create_user(
               full_name=fullname,
               password=password,
               email=email,
               )
               return redirect("account:login")
          return render(request, self.template_name, {})


class LoginView(View):
     template_name = "account/login.html"

     def get(self, request, *args, **kwargs):
          if self.request.user.is_authenticated:
               if self.request.user.admin:
                    return redirect("account:profile")
               else:
                    return redirect("home")
          return render(request, self.template_name, {})

     def post(self, request, *args, **kwargs):
          if request.method == "POST":
               print("well the requst is the post")
               print(request.POST)
               email = request.POST.get("email")
               password = request.POST.get("password")
               is_user = User.objects.filter(email=email)
               is_form_correct = (email is None or password is None)
               if is_form_correct:
                    messages.error(self.request, "Please enter your data correctly")
                    return render(request, self.template_name, {})
               if is_user.exists():
                    user = is_user.first()
                    if user.is_active:
                         authenticated_user = authenticate(request, username=email, password=password)
                         if authenticated_user is not None:
                              login(request, authenticated_user)
                              if authenticated_user.admin:
                                   return redirect('account:profile')
                              return redirect('home')
                         else:
                              messages.error(
                              request,
                              "Invalid Credentials",
                              )
                              # return render(request, self.template_name, {})
                         
                    else:
                         messages.error(
                         request,
                         "User is not activated. Send OTP to activate",
                         )
                         # return render(request, self.template_name, {})
               else:
                    messages.error(
                    request,
                    "User does not exist!",
                    )
                    # return render(request, self.template_name, {})
                    
               
          return render(request, self.template_name, {})
     

class AdminUerList(ListView):
     template_name = 'account/admin/user_list.html'
     queryset = User.objects.filter(admin=False)
     paginate_by = 5


class AdminUserDetail(DetailView):
     template_name = 'account/admin/user_detail.html'
     model = User
