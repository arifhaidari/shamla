from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from datetime import date, datetime, timedelta
from cart.models import Cart, CartProduct, WishList, WishListItem
from django.db.models import Q
from newsletter.models import CustomerMessage, MailingList
from product.models import Category, Color, Product, Size
from marketing.models import Slider, Brand, Recommendation, NewArrival
from shamla.utils import empty_none_validator, is_newsletter



class HomePage(View):
     template_name = 'home/home_page.html'
     
     def get_data(self, request):
          try:
               recommended_object = Recommendation.objects.first()
               recommended_item_number = recommended_object.item_number
               recommended_categories = recommended_object.category.all().order_by('-id')
          except:
               recommended_categories = Category.objects.all()[:3]
               recommended_item_number = 16
          recommended = {}
          for category in recommended_categories:
               recommended[category.name] = Product.objects.filter(category__name__icontains=category.name)[:recommended_item_number]
          
          # new arrival
          try:
               new_arrival_object = NewArrival.objects.first()
               new_arrival_item_number = new_arrival_object.item_number
               raw_value_days = date.today() - new_arrival_object.time_interval
               new_arrival_time_interval = datetime.today() - timedelta(days=raw_value_days.days)
          except:
               print('insdie the exciept ')
               new_arrival_time_interval = datetime.today() - timedelta(days=90)
               new_arrival_item_number = 16
               
          new_arrival_list = Product.objects.filter(updated__range=(new_arrival_time_interval, date.today()))[:new_arrival_item_number]
          data = {
               'recommended': recommended, 
               'new_arrivals': new_arrival_list,
               'sliders': Slider.objects.all(),
               'brands': Brand.objects.all(),
               'cart_data': get_cart_brief_items(request),
               'is_newsletter': is_newsletter(request, MailingList),
               }
          return data
     
     def get(self, request, *args, **kwargs):
          # get three most sold category and show them in recommended
          data = self.get_data(request)
          return render(request, self.template_name, data)
     
     def post(self, request, *args, **kwargs):
          newsletter_registration(request)
          data = self.get_data(request)
          return render(request, self.template_name, data)

def newsletter_registration(request):
     if request.method == 'POST':
          print('value of post')
          email = request.POST.get('email', None)
          if empty_none_validator([email]):
               MailingList.objects.create_mailing(request=request, email=email)

class About(View):
     template_name = 'home/about.html'
     
     def get_data(self, request):
          the_data = {
               'brands': Brand.objects.all(),
               'cart_data': get_cart_brief_items(request),
               'is_newsletter': is_newsletter(request, MailingList),
          }
          return the_data
     
     def get(self, request, *args, **kwargs):
          the_data = self.get_data(request)
          return render(request, self.template_name, the_data)
     
     def post(self, request, *args, **kwargs):
          newsletter_registration(request)
          data = self.get_data(request)
          return render(request, self.template_name, data)
     
class Contact(View):
     template_name = 'home/contact.html'
     
     def the_cart_data(self):
          return {
               'cart_data': get_cart_brief_items(self.request),
          } 
     
     def get(self, request, *args, **kwargs):
          the_data = self.the_cart_data()
          return render(request, self.template_name, the_data)
     
     def post(self, request, *args, **kwargs):
          the_data = self.the_cart_data()
          print('vale of request.POST')
          print(request.POST)
          if request.method == 'POST':
               name = request.POST.get('name', None)
               email = request.POST.get('email', None)
               message = request.POST.get('message', None)
               is_valid = empty_none_validator([name, email, message])
               if is_valid:
                    user = None
                    if request.user.is_authenticated:
                         user = request.user
                    CustomerMessage.objects.create(user=user, name=name, email=email, message=message)
                    messages.success(request, 'Your message has been sent successfully')
               else:
                    print('here is errro ')
                    messages.error(request, 'Fill inputs properly')
          return render(request, self.template_name, the_data)


def get_cart_brief_items(request):
     cart_obj, new_obj = Cart.objects.new_or_get(request)
     the_response = {
          'is_error': True
     }
     if cart_obj is not None:
          request.session['cart_items'] = cart_obj.current_item_num
          try:
               the_query = cart_obj.cartproduct_set.all().order_by('-id')
               print('value fo the_query')
               the_response['queryset'] = the_query
               categories = Category.objects.filter(active=True).order_by('-id')[:30]
               the_response['categories'] = categories
               the_response['category_divider'] = int(len(categories) / 2) + 1
               the_response['is_error'] = False
          except:
               pass
     return the_response

# Wish list 

def update_wish_list(request):
     response_data = {
          "is_error": True,
          }
     if request.method == 'POST':
          product_id = request.POST.get('product_id', None)
          size_id = request.POST.get('size_id', None)
          color_id = request.POST.get('color_id', None)
          print('valeu fo request')
          print(request.POST)
          size = None
          color = None
          if product_id != '' and product_id is not None:
               wishlist, created = WishList.objects.get_or_create(user=request.user)
               try:
                    the_product = Product.objects.get(id=product_id)
                    
                    the_filter = Q(product=the_product, wishlist=wishlist)
                    if size_id is not None and size_id != '':
                         size = Size.objects.get(id=size_id) or None
                         the_filter = the_filter.add(Q(size__id=size_id), Q.AND)
                    if color_id is not None and color_id != '':
                         color = Color.objects.get(id=color_id) or None
                         the_filter = the_filter.add(Q(color__id=color_id), Q.AND)
                    the_wish_list = WishListItem.objects.filter(the_filter)
                    if not the_wish_list.exists():
                         WishListItem.objects.create(
                              wishlist = wishlist, product = the_product,
                              size = size, color=color
                         )
                    response_data['is_error'] = False
               except:
                    pass
     return JsonResponse(response_data, status=200)

class WishItemList(View):
     template_name = 'home/wish_list.html'
     # model = CartProduct
     
     def get(self, request, *args, **kwargs):
          wishlist, created = WishList.objects.get_or_create(user=request.user)
          print('value of wishlist')
          print(wishlist)
          queryset = WishListItem.objects.filter(wishlist=wishlist)
          the_data = {
               'cart_data': get_cart_brief_items(request),
               'object_list': queryset,
          }
          print('value of queryset')
          print(queryset)
          return render(request, self.template_name, the_data)
     
     def post(self, request, *args, **kwargs):
          response_data = {
          "is_error": True,
          "is_new_product": False,
          }
          if request.method == 'POST':
               wish_id = request.POST.get('wish_id', None)
               quantiy = request.POST.get('quantity', None)
               the_quantity = 1
               if quantiy is not None and quantiy != '':
                    the_quantity = int(quantiy) or 1
               print('valeu fo request')
               print(request.POST)
               if wish_id != '' and wish_id is not None:
                    try:
                         wishlist_item = WishListItem.objects.get(id=wish_id)
                         cart_obj, new_obj = Cart.objects.new_or_get(request)
                         product_obj= wishlist_item.product
                         the_filter = Q(product=product_obj, cart=cart_obj)
                         if wishlist_item.size is not None:
                              the_filter = the_filter.add(Q(size=wishlist_item.size), Q.AND)
                         if wishlist_item.color is not None:
                              the_filter = the_filter.add(Q(color=wishlist_item.color), Q.AND)
                         cart_product_obj_raw = CartProduct.objects.filter(the_filter)
                         if cart_product_obj_raw.exists():
                              cart_product = cart_product_obj_raw.first()
                              cart_product.product_quantity += the_quantity
                              cart_product.save()
                         else:
                              print('create new ---======')
                              cart_product = CartProduct.objects.create(
                                   cart= cart_obj, product=product_obj, product_quantity=the_quantity,
                                   product_price= product_obj.price or 0, product_purchase_price=product_obj.purchase_price or 0,
                                   product_discount=product_obj.discount_amount
                              )
                              if cart_product is not None:
                                   print('new_cart_product_obj is not none')
                                   if wishlist_item.size is not None:
                                        cart_product.size = wishlist_item.size or None
                                   if wishlist_item.color is not None:
                                        cart_product.color = wishlist_item.color or None
                                   cart_product.save()
                                   response_data['is_new_product'] = True
                         WishListItem.objects.get(id=wish_id).delete()
                         response_data['is_error'] = False
                         the_dic = update_cart_front_end(response_data, cart_obj, request, cart_product)
                         response_data = {**response_data, **the_dic}
                    except:
                         pass
          return JsonResponse(response_data, status=200)



def update_cart_front_end(response_data, cart_obj, request, cart_product):
     print('inside the update_cart_front_end')
     the_cart_num = cart_obj.current_item_num
     request.session['cart_items'] = the_cart_num
     response_data['cart_item_num'] = the_cart_num
     if response_data['is_new_product']:
          print('here is new product-=------')
          response_data['image_url'] = cart_product.product.productimages_set.first().image.url
          response_data['product_title'] = cart_product.product.title
          response_data['product_price'] = cart_product.product_price
          if cart_product.size is not None:
               response_data['product_size'] = cart_product.size.name
          else:
               response_data['product_size'] = 'Free Size'
          if cart_product.color is not None:
               response_data['product_color'] = cart_product.color.name
          else:
               response_data['product_color'] = 'No Color'
          response_data['product_id'] = cart_product.product.id
          response_data['product_quantity'] = cart_product.product_quantity
          response_data['the_url'] = cart_product.product.get_absolute_url()
          # for cart home page
          response_data['total_discount'] = cart_product.total_discount
          response_data['total_price'] = cart_product.total_price
     else:
          print('here is old ===== product')
          print(cart_product.product_quantity)
          response_data['product_quantity'] = cart_product.product_quantity
          response_data['total_discount'] = cart_product.total_discount
          response_data['total_price'] = cart_product.total_price
          response_data['product_id'] = cart_product.product.id
     response_data['cart_subtotal'] = cart_obj.subtotal
     response_data['cart_discount'] = cart_obj.discount_total
     response_data['cart_total'] = cart_obj.total
     response_data['shipment_fee'] = cart_obj.shipment_fee
     return response_data


# def register_to_newsletter(request):
#      print('inside the register to newsletter')
#      if request.method == 'POST':
#           print('it is post')
          
#      redirect('home')


