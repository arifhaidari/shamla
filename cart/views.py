import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, get_user_model, login
from django.db.models import Q
from django.utils.translation import activate
from django.views.generic import View, ListView, UpdateView, DetailView, DeleteView
from address.models import Address
from billing.models import BillingProfile
from order.models import Order, ShipmentMethod
from product.models import Product, Color, Size
from shamla.views import get_cart_brief_items, update_cart_front_end
from .models import Cart, CartProduct
from django.contrib import messages
from decimal import Decimal

User = get_user_model()


def clear_cart(request):
     response_data = {
               "is_error": True,
               }
     if request.method == 'POST':
          cart_obj, new_obj = Cart.objects.new_or_get(request)
          if cart_obj is not None:
               CartProduct.objects.filter(cart=cart_obj).delete()
               cart_obj.shipment_fee = 0
               cart_obj.save()
               response_data['is_error'] = False
     return JsonResponse(response_data)

def cart_update(request):
     print('value fo request.POST')
     print(request.POST)
     product_id = request.POST.get('product_id', None)
     operation = request.POST.get('operation', None)
     quantity = request.POST.get('quantity', None)
     size_id = request.POST.get('size_id', None)
     color_id = request.POST.get('color_id', None)
     the_quantity = int(quantity) or 1
     response_data = {
          "is_error": True,
          "is_new_product": False,
          }
     if product_id is not None and product_id != '':
          try:
               product_obj = Product.objects.get(id=product_id) or None
          except Product.DoesNotExist:
               pass
          cart_obj, new_obj = Cart.objects.new_or_get(request)
          if product_obj is not None and cart_obj is not None:
               response_data['is_error'] = False
               the_filter = Q(product=product_obj, cart=cart_obj)
               if size_id is not None and size_id != '':
                    the_filter = the_filter.add(Q(size__id=size_id), Q.AND)
               if color_id is not None and color_id != '':
                    the_filter = the_filter.add(Q(color__id=color_id), Q.AND)
               cart_product_obj_raw = CartProduct.objects.filter(the_filter)
               if cart_product_obj_raw.exists():
                    cart_product = cart_product_obj_raw.first()
                    if operation == 'add':
                         print('add up the quantity ')
                         cart_product.product_quantity += the_quantity
                    else:
                         print('minus down the quantity ')
                         if cart_product.product_quantity > 1:
                              cart_product.product_quantity -= 1
                    cart_product.save()
               else:
                    print('create new ---======')
                    try:
                         cart_product = CartProduct.objects.create(
                              cart= cart_obj, product=product_obj, product_quantity=the_quantity,
                              product_price= product_obj.price or 0, product_purchase_price=product_obj.purchase_price or 0,
                              product_discount=product_obj.discount_amount
                         )
                         if cart_product is not None:
                              print('new_cart_product_obj is not none')
                              if size_id is not None and size_id != '':
                                   cart_product.size = Size.objects.get(id=size_id) or None
                              if color_id is not None and color_id != '':
                                   cart_product.color = Color.objects.get(id=color_id) or None
                              cart_product.save()
                              response_data['is_new_product'] = True
                    except:
                         print('erorr occured in creating new one')
                         pass
               the_dic = update_cart_front_end(response_data, cart_obj, request, cart_product)
               response_data = {**response_data, **the_dic}
               return JsonResponse(response_data, status=200) # HttpResponse
               # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
     return JsonResponse(response_data, status=200)


class CartItemList(View):
     template_name = 'cart/cart_home.html'
     # model = CartProduct
     
     def the_data(self, request):
          cart_obj, new_obj = Cart.objects.new_or_get(request)
          cart_items = CartProduct.objects.filter(cart=cart_obj).order_by('-id')
          cart_data = get_cart_brief_items(request)
          shipment_method_list = ShipmentMethod.objects.order_by('-id')
          context = {
               'object_list': cart_items,
               'cart_data': cart_data,
               'shipment_method_list': shipment_method_list,
          }
          return context
     
     
     def get(self, request, *args, **kwargs):
          print('insid eth self.the_data(self.request)')
          # print(self.the_data(self.request))
          context = self.the_data(request)
          return render(request, self.template_name, context)
     
     def post(self, request, *args, **kwargs):
          # context = self.the_data(self.request)
          print('value fo request------')
          print(request.POST)
          is_not_valid = False
          if request.method == 'POST':
               selected_fee = request.POST.get('select_shipment_fee', None)
               is_not_valid = selected_fee == '' or selected_fee is None
               try:
                    the_fee = Decimal(selected_fee) 
               except Exception as e:
                    is_not_valid = True
               if not is_not_valid:
                    cart_obj, new_obj = Cart.objects.new_or_get(request)
                    cart_obj.shipment_fee = the_fee
                    cart_obj.save()
                    return redirect('cart:checkout')
               else:
                    print('in the default return ')
                    messages.error(self.request, 'Select a payment method')
          
          return render(request, self.template_name, self.the_data(self.request))

class Checkout(View):
     template_name = 'cart/check_out_home.html'
     
     def get(self, request, *args, **kwargs):
          the_data = get_cart_data(request, request.user)
          if len(the_data['cart_data']['queryset']) == 0:
               return redirect('cart:item_list')
          return render(request, self.template_name, the_data)
     
     def post(self, request, *args, **kwargs):
          print('value of request in post')
          print(request.user)
          raw_data = request.POST
          print(request.POST)
          user = request.user if request.user.is_authenticated else None
          the_data = get_cart_data(request, request.user)
          # user login start
          email = request.POST.get("login_email", None)
          password = request.POST.get("login_password", None)
          is_login_form_exist = email is not None and password is not None
          if is_login_form_exist and user is None:
               is_form_correct = email == '' or password == ''
               if is_form_correct:
                    messages.error(request, 'Enter your credential properly')
                    return render(request, self.template_name, the_data)
               user, message = on_checkout_login(request, email, password)
               if user is not None:
                    messages.success(request, message)
                    the_data = get_cart_data(request, user)
               else:
                    messages.error(request, message)
               return render(request, self.template_name, the_data)
          # End user login
          # 
          # user registration sart
          cart_obj, new_obj = Cart.objects.new_or_get(request)
          is_create_account = raw_data.get('account', None)
          if is_create_account is not None and is_create_account == 'on' and user is None:
               print('it is create_user_on_fly')
               user = create_user_on_fly(request, raw_data)
               if user is None:
                    messages.error(request, 'Enter user information properly for registration')
                    return render(request, self.template_name, the_data)
               the_data = get_cart_data(request, user)
          # End user registration
          if user is None:
               messages.error(request, 'User is not authenticated. Please Login or check the create account down below')
               return render(request, self.template_name, the_data)
          # //
          billing_address_select = raw_data.get('billing_address_select', None)
          shipping_address_select = raw_data.get('shipping_address_select', None)
          order_note = raw_data.get('order_note', None)
          is_shipping = raw_data.get('shipping', None)
          
          # create billing profile
          billing_profile_object, created = BillingProfile.objects.get_or_create(user=user)
          print('////')
          print(billing_address_select)
          print(shipping_address_select)
          print(is_shipping)
          print(is_create_account)
          final_order_object = None
          the_type = 'both'
          billing_address_obj = get_create_address(the_type, raw_data, billing_profile_object)
          if billing_address_obj is None:
               messages.error(request, 'Enter billing address information properly')
               return render(request, self.template_name, the_data)
          if is_shipping is not None and is_shipping == 'on':
               the_type = 'billing'
               shipping_address_obj = get_create_address('shipping', raw_data, billing_profile_object)
               if shipping_address_obj is None:
                    messages.error(request, 'Enter shipping address information properly')
                    return render(request, self.template_name, the_data)
               else:
                    order_object = place_order(order_note, billing_address_obj, cart_obj, billing_profile_object)
                    if order_object is None:
                         messages.error(request, 'Uknonwn Error Occured. Please try again')
                         return render(request, self.template_name, the_data)
                    order_object.shipping_address = shipping_address_obj
                    order_object.save()
                    final_order_object = order_object
          else:
               place_order_obj = place_order(order_note, billing_address_obj, cart_obj, billing_profile_object)
               if place_order_obj is None:
                    messages.error(request, 'Uknonwn Error Occured. Please try again')
                    return render(request, self.template_name, the_data)
               final_order_object = place_order_obj
          # messages.success(request, 'Order placed successfully')
          if final_order_object is None:
               messages.error(request, 'Unknown Error Occured')
          return redirect('billing:order_summary', order_id=final_order_object.order_id) if final_order_object is not None else render(request, self.template_name, the_data)


def on_checkout_login(request, email, password):
     print('value of on_checkout_login')
     print(email, password)
     is_user = User.objects.filter(email=email)
     if is_user.exists():
          user = is_user.first()
          if user.is_active:
               authenticated_user = authenticate(request, username=email, password=password)
               if authenticated_user is not None:
                    login(request, authenticated_user)
                    print('value fo authenticated_user')
                    print(authenticated_user)
                    return authenticated_user, 'Logged in successfully!!!'
               else:
                    return None, 'Invalid Credentials'
               
          else:
               return None, 'User is not activated'
     return None, 'User deos not exist'


def get_cart_data(request, user):
     cart_data = get_cart_brief_items(request)
     addresses = None
     if user.is_authenticated:
          print('yes user is authenticated')
          addresses = Address.objects.filter(billing_profile__user=user)
     the_data = {
          'cart_data': cart_data,
          'addresses': addresses,
     }
     return the_data
# when order is placed then subtract the sold items from product quantity 


def create_user_on_fly(request, raw_data):
     email = raw_data.get('billing_email', None)
     password = raw_data.get('register_password', None)
     confirm_password = raw_data.get('register_confirm_password', None)
     full_name = raw_data.get('billing_full_name', None)
     
     if (email == '' or password == '' or confirm_password == '' or full_name == ''
         or password != confirm_password):
          return None
     new_user = User.objects.create_user(
          full_name=full_name, password=password, email=email
     )
     if new_user is not None:
          authenticated_user = authenticate(request, username=email, password=password)
          if authenticated_user is not None:
               login(request, authenticated_user)
               return authenticated_user
     return None


# maybe place order after successing the payemnt or just mark it as paid after success
def place_order(order_note, address_object, cart_object, billing_profile_object):
     if address_object is None or cart_object is None:
          return None
     # delete all the order prevously created with this cart_object
     Order.objects.filter(cart=cart_object).delete()
     # create new Order
     order_obj, created = Order.objects.get_or_create(
          cart=cart_object, billing_profile=billing_profile_object,
          active=True, status=Order.OrderStatus.Created
     )
     order_obj.order_note=order_note if order_note is not None and order_note != '' else None
     order_obj.billing_address=address_object
     order_obj.save()
     # delelte previous Orders if there is any
     Order.objects.filter(billing_profile=billing_profile_object, status=Order.OrderStatus.Created).exclude(cart=cart_object).delete()
     return order_obj

address_type_dict = {
     'billing': 'Billing',
     'shipping': 'Shipping',
     'both': 'Both',
}

def get_create_address(raw_type, raw_data, billing_profile_object):
     print('inside the get_create_address')
     print(raw_type)
     if raw_type == 'both':
          the_type = 'billing'
     else:
          the_type = raw_type
     full_name = raw_data.get(f"{the_type}_full_name", None)
     company_name = raw_data.get(f"{the_type}_company", None)
     country = raw_data.get(f"{the_type}_country", None)
     city = raw_data.get(f"{the_type}_city", None)
     district = raw_data.get(f"{the_type}_district", None)
     zipcode = raw_data.get(f"{the_type}_zipcode", None)
     street = raw_data.get(f"{the_type}_street", None)
     apartment = raw_data.get(f"{the_type}_apartment", None)
     phone = raw_data.get(f"{the_type}_phone", None)
     email = raw_data.get(f"{the_type}_email", None)
     is_not_valid = (full_name == '' or country == '' or city == '' or district == '' 
                 or zipcode == '' or street == '' or phone == '' or email == '')
     if is_not_valid:
          return None
     # first create a billing_profile if not created
     address_object, created = Address.objects.get_or_create(
          billing_profile=billing_profile_object, full_name=full_name, 
          country=country, city=city, district=district, phone=phone,
          company=company_name if company_name != '' else None, 
          apartment= apartment if apartment != '' else None,
          street=street, email=email, zipcode=zipcode
     )
     address_object.address_type=address_type_dict[the_type]
     address_object.save()
     return address_object


