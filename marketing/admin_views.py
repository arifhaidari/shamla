from django.contrib.messages.api import error
from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView, View
from datetime import date, datetime, timedelta
# from dateutil.relativedelta import relativedelta

from product.models import Category

from django.contrib import messages
from .models import (
     Slider, Brand, SpecialOffer, CoolCustomerDiscount, Recommendation, NewArrival
     )


class ManageRecommendation(View):
     template_name = 'marketing/admin/recommendation_page.html'
     
     def get(self, request, *args, **kwrags):
          data = {
               'categories': Category.objects.order_by('-id'),
               'recommendation': Recommendation.objects.first() or None,
               'new_arrival': NewArrival.objects.first() or None,
          }
          return render(request, self.template_name, data)
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               the_category_select = request.POST.getlist('the_category_select', None)
               recommend_item_number = request.POST.get('recommend_item_number', None)
               recommendation_id = request.POST.get('recommendation_id', None)
               new_arrival_id = request.POST.get('new_arrival_id', None)
               time_interval = request.POST.get('time_interval', None)
               new_arrival_item_number = request.POST.get('new_arrival_item_number', None)
               is_true = (
                    the_category_select is None or the_category_select == '' or recommend_item_number is None or recommend_item_number == '' 
                    or time_interval is None or time_interval == '' or new_arrival_item_number is None or new_arrival_item_number == '' 
                    )
               if is_true:
                    messages.error(request, 'Enter requried fields i.e. Category, Item Number and time interval')
               else:
                    date = datetime.strptime(time_interval, "%Y-%m-%d").date()
                    today_date = date.today()
                    result = today_date - date
                    try:
                         # new arrival
                         arrival_item_number = int(new_arrival_item_number)
                         print(arrival_item_number)
                         if int(result.days) > 7 and arrival_item_number <= 30:
                              if new_arrival_id == '':
                                   NewArrival.objects.create(time_interval=time_interval, item_number=arrival_item_number)
                              else:
                                   new_arrival_object = NewArrival.objects.get(id=new_arrival_id)
                                   new_arrival_object.time_interval = time_interval
                                   new_arrival_object.item_number = arrival_item_number
                                   new_arrival_object.save()
                         else:
                              messages.error(request, 'Time travel should be greater than at least a week and item number should be less than 30')
                         # recommned category
                         if len(the_category_select) < 3:
                              messages.error(request, 'You should select three categories')
                         else:
                              the_item_number = int(recommend_item_number)
                              print(the_item_number)
                              if the_item_number <= 30:
                                   if recommendation_id == '':
                                        new_recommend = Recommendation.objects.create(item_number=the_item_number)
                                        save_recommend_category(new_recommend, the_category_select[0:3])
                                   else:
                                        recommend_object = Recommendation.objects.get(id=recommendation_id)
                                        recommend_object.item_number = the_item_number
                                        recommend_object.save()
                                        recommend_object.category.clear()
                                        save_recommend_category(recommend_object, the_category_select[0:3])
                              else:
                                   messages.error(request, 'Item number of recommendation should be less than 30')
                    except:
                         messages.error(request, 'Unknown error occured. Try Again')
                         
          new_data = {
               'categories': Category.objects.order_by('-id'),
               'recommendation': Recommendation.objects.first() or None,
               'new_arrival': NewArrival.objects.first() or None,
          }          
          return render(request, self.template_name, new_data)

def save_recommend_category(recommend_object, the_select):
     for the_id in the_select:
          try:
               category = Category.objects.get(id=the_id)
               recommend_object.category.add(category)
          except:
               pass

# Slider
class AdminSliderListView(ListView):
     template_name = 'marketing/admin/admin_slider_list.html'
     queryset = Slider.objects.all().order_by('-id')

class AdminCreateSlider(View):
     template_name = 'marketing/admin/admin_create_slider.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               image = request.FILES.get('image', None)
               title = request.POST.get('title', None)
               subtitle = request.POST.get('subtitle', None)
               check_box = request.POST.get('is_active', None)
               if title is None or title == '' or subtitle is None or subtitle == '' or image is None or image == '':
                    messages.error(self.request, "Title, image or Subtitle field is empty")
               else:
                    is_active = check_box is not None
                    try:
                         Slider.objects.create(title=title, subtitle=subtitle, image=image, active=is_active)
                         messages.success(self.request, "Slider data is saved successfully!")
                    except:
                         messages.error(self.request, "Error: Only 25 characters are allowed")
          return render(request, self.template_name, {})


class AdminUpdateSlider(UpdateView):
     template_name = 'marketing/admin/admin_update_slider.html'
     model = Slider
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               image = request.FILES.get('image', None)
               print('value of image in update')
               print(image)
               title = request.POST.get('title', None)
               subtitle = request.POST.get('subtitle', None)
               check_box = request.POST.get('is_active', None)
               if title is None or title == '' or subtitle is None or subtitle == '':
                    messages.error(self.request, "Title or Subtitle field is empty")
               else:
                    try:
                         obj = self.get_object()
                         is_active = check_box is not None
                         obj.title = title
                         obj.subtitle = subtitle
                         obj.active = is_active
                         if image is not None and image != '':
                              print('new image is uploaded bro')
                              obj.image = image
                         obj.save()
                         return redirect('marketing:admin_slider_list')              
                    except:
                         messages.error(self.request, "Error: Only 25 characters are allowed")
          return render(request, self.template_name, {'object': self.get_object()})


# Brand
class AdminBrandListView(ListView):
     template_name = 'marketing/admin/admin_brand_list.html'
     queryset = Brand.objects.all().order_by('-id')

class AdminCreateBrand(View):
     template_name = 'marketing/admin/admin_create_brand.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               logo = request.FILES.get('logo', None)
               name = request.POST.get('name', None)
               web = request.POST.get('web', None)
               check_box = request.POST.get('is_active', None)
               if name is None or name == '' or web is None or web == '' or logo is None or logo == '':
                    messages.error(self.request, "Name, Logo or Web field is empty")
               else:
                    is_active = check_box is not None
                    try:
                         Brand.objects.create(name=name, web=web, logo=logo, active=is_active)
                         messages.success(self.request, "Brand data is saved successfully!")
                    except:
                         messages.error(self.request, "Error: Some Unknown Error Happened. Try Again!")
          return render(request, self.template_name, {})


class AdminUpdateBrand(UpdateView):
     template_name = 'marketing/admin/admin_update_brand.html'
     model = Brand
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               logo = request.FILES.get('logo', None)
               print('value of logo in update')
               print(logo)
               name = request.POST.get('name', None)
               web = request.POST.get('web', None)
               check_box = request.POST.get('is_active', None)
               if name is None or name == '' or web is None or web == '':
                    messages.error(self.request, "Name or Web field is empty")
               else:
                    try:
                         obj = self.get_object()
                         is_active = check_box is not None
                         obj.name = name
                         obj.web = web
                         obj.active = is_active
                         if logo is not None and logo != '':
                              print('new logo is uploaded bro')
                              obj.logo = logo
                         obj.save()
                         return redirect('marketing:admin_brand_list')              
                    except:
                         messages.error(self.request, "Error: Some Unknown Error Happened. Try Again.")
          return render(request, self.template_name, {'object': self.get_object()})


# Cool Customer Discount
class AdminCoolCustomerListView(ListView):
     template_name = 'marketing/admin/admin_cool_list.html'
     queryset = CoolCustomerDiscount.objects.all()

class AdminCreateCoolCustomer(View):
     template_name = 'marketing/admin/admin_create_cool.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               trigger_amount = request.POST.get('trigger_amount', None)
               discount_by_amount = request.POST.get('discount_by_amount', None)
               discount_by_percentage = request.POST.get('discount_by_percentage', None)
               check_box = request.POST.get('is_active', None)
               if trigger_amount is None or trigger_amount == '':
                    messages.error(self.request, "Trigger amount field is empty")
               elif (discount_by_percentage is None or discount_by_percentage == '') and (discount_by_amount is None or discount_by_amount == ''):
                    messages.error(self.request, 'You should provide discount method either by percentage or by amount')
               elif (discount_by_percentage is not None and discount_by_percentage != '') and (discount_by_amount is not None and discount_by_amount != ''):
                    messages.error(self.request, 'You can provide only one discount method. Either amount or percentage!')
               else:
                    is_object_exist = CoolCustomerDiscount.objects.all()
                    if len(is_object_exist) != 0:
                         messages.error(self.request, 'You have already created Cool Custmer Discoun method. You can edit that one instead of creating new one!')
                    else:
                         is_active = check_box is not None
                         is_percentage = discount_by_percentage is not None and discount_by_percentage != ''
                         try:
                              if is_percentage:
                                   percentage_value = int(discount_by_percentage)
                                   if percentage_value > 60:
                                        messages.error(self.request, 'Percentage should not be greater than 60')
                                        return render(request, self.template_name, {})
                                   CoolCustomerDiscount(trigger_amount=trigger_amount, discount_by_percentage= discount_by_percentage, active=is_active).save()
                              else:
                                   CoolCustomerDiscount(trigger_amount=trigger_amount, discount_by_amount= discount_by_amount, active=is_active).save()
                              # messages.success(self.request, "Cool Customer data is saved successfully!")
                              return redirect('marketing:admin_cool_list')
                         except:
                              messages.error(self.request, "Error: Uknown Error Occured")
          return render(request, self.template_name, {})


class AdminUpdateCoolCustomer(UpdateView):
     template_name = 'marketing/admin/admin_update_cool.html'
     model = CoolCustomerDiscount
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               trigger_amount = request.POST.get('trigger_amount', None)
               discount_by_amount = request.POST.get('discount_by_amount', None)
               discount_by_percentage = request.POST.get('discount_by_percentage', None)
               check_box = request.POST.get('is_active', None)
               if trigger_amount is None or trigger_amount == '':
                    messages.error(self.request, "Trigger amount field is empty")
               elif (discount_by_percentage is None or discount_by_percentage == '') and (discount_by_amount is None or discount_by_amount == ''):
                    messages.error(self.request, 'You should provide discount method either by percentage or by amount')
               elif (discount_by_percentage is not None and discount_by_percentage != '') and (discount_by_amount is not None and discount_by_amount != ''):
                    messages.error(self.request, 'You can provide only one discount method. Either amount or percentage!')
               else:
                    obj = self.get_object()
                    is_active = check_box is not None
                    is_percentage = discount_by_percentage is not None and discount_by_percentage != ''
                    try:
                         obj.trigger_amount = trigger_amount
                         obj.active = is_active
                         if is_percentage:
                              percentage_value = int(discount_by_percentage)
                              if percentage_value > 60:
                                   messages.error(self.request, 'Percentage should not be greater than 60')
                                   return render(request, self.template_name, {})
                              obj.discount_by_percentage = percentage_value
                         else:
                              obj.discount_by_amount = discount_by_amount
                         obj.save()
                         return redirect('marketing:admin_cool_list') 
                    except:
                         messages.error(self.request, "Error: Uknown Error Occured. Try Again!")
          return render(request, self.template_name, {'object': self.get_object()})


# Special Offer
class AdminSpecialOfferListView(ListView):
     template_name = 'marketing/admin/admin_special_list.html'
     queryset = SpecialOffer.objects.all()

class AdminCreateSpecialOffer(View):
     template_name = 'marketing/admin/admin_create_special.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               event = request.POST.get('event', None)
               discount_by_percentage = request.POST.get('discount_by_percentage', None)
               check_box = request.POST.get('is_active', None)
               if event is None or event == '' or discount_by_percentage is None or discount_by_percentage == '':
                    messages.error(self.request, "Event or Discount Percentage field is empty")
               else:
                    is_object_exist = SpecialOffer.objects.all()
                    if len(is_object_exist) != 0:
                         messages.error(self.request, 'You have already created Special Offer Discoun method. You can edit that one instead of creating new one!')
                    else:
                         is_active = check_box is not None
                         try:
                              print('value of discount_by_percentage')
                              print(discount_by_percentage)
                              percentage_value = int(discount_by_percentage)
                              if percentage_value > 60:
                                   messages.error(self.request, 'Percentage should not be greater than 60')
                                   return render(request, self.template_name, {})
                              SpecialOffer(event=event, discount_by_percentage=percentage_value, active=is_active).save()
                              return redirect('marketing:admin_special_list') 
                         except:
                              messages.error(self.request, "Error: Some Unknown Error Happened. Try Again!")
          return render(request, self.template_name, {})


class AdminUpdateSpecialOffer(UpdateView):
     template_name = 'marketing/admin/admin_update_special.html'
     model = SpecialOffer
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               evet = request.POST.get('event', None)
               discount_by_percentage = request.POST.get('discount_by_percentage', None)
               check_box = request.POST.get('is_active', None)
               if evet is None or evet == '' or discount_by_percentage is None or discount_by_percentage == '':
                    messages.error(self.request, "Event or Discount Percentage field is empty")
               else:
                    try:
                         percentage_value = int(discount_by_percentage)
                         if percentage_value > 60:
                              messages.error(self.request, 'Percentage should not be greater than 60')
                              return render(request, self.template_name, {})
                         obj = self.get_object()
                         obj.event = evet
                         obj.discount_by_percentage = discount_by_percentage
                         obj.active = check_box is not None
                         obj.save()
                         return redirect('marketing:admin_special_list')              
                    except:
                         messages.error(self.request, "Error: Some Unknown Error Happened. Try Again.")
          return render(request, self.template_name, {'object': self.get_object()})


