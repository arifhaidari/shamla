import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DetailView, DeleteView
from django.views.generic.dates import timezone_today
from cart.models import Cart, CartProduct, WishListItem
from marketing.models import Slider, Brand
from django.contrib.auth.decorators import login_required

from newsletter.models import NewsLetter, NewsLetterType
from .models import Product, Category, ProductImages, Size, Color, Tag
from order.models import ShipmentMethod

# product
class AdminProductView(ListView):
     template_name = 'product/admin/admin_product_list.html'
     queryset = Product.objects.order_by('-id')


class AdminProductDetail(DetailView):
     model = Product
     template_name = 'product/admin/admin_product_detail.html'

class AdminCreateProduct(View):
     template_name = 'product/admin/admin_create_product.html'
     data = {
               'categories': Category.objects.order_by('-id'),
               'colors': Color.objects.order_by('-id'),
               'sizes': Size.objects.order_by('-id'),
               'tags': Tag.objects.order_by('-id'),
          }
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, self.data)
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               raw_data = request.POST
               images = request.FILES.getlist('product_images', None)
               title = raw_data.get('title', None)
               price = raw_data.get('price', None)
               stock = raw_data.get('stock', None)
               old_price = raw_data.get('old_price', None)
               purchase_price = raw_data.get('purchase_price', None)
               discount_percentage = raw_data.get('discount_percentage', None)
               description = raw_data.get('description', None)
               check_box = raw_data.get('is_active', None)
               is_true = (
                    title is None or title == '' or images is None or len(images) <= 0 or 
                    price is None or price == '' or stock is None or stock == '' or 
                    description is None or description == '' or purchase_price is None or purchase_price == ''
                    )
               if is_true:
                    messages.error(self.request, "Please fill required fields i.e. title, price, images, stock, and description")
               else:
                    messages.success(self.request, "Product created successfully!")
                    is_active = check_box is not None
                    new_product = None
                    try:
                         new_product = Product.objects.create(
                              title=title, active=is_active, price=float(price), 
                              stock=int(stock), description=description, purchase_price=float(purchase_price)
                              )
                    except:
                         messages.error(self.request, 'Unknown Error occured. Enter your input values correctly!')
                         return render(request, self.template_name, self.data)
                    if new_product is not None:
                         if old_price is not None and old_price != '':
                              try:
                                   old_price_value = float(old_price)
                                   new_product.old_price = old_price_value
                              except:
                                   messages.error(self.request, 'Old price should be digit')
                         if discount_percentage is not None and discount_percentage != '':
                              try:
                                   discount_value = int(discount_percentage)
                                   if discount_value <= 0 or discount_value > 60:
                                        messages.error(self.request, 'Discount Percentage should be between 1 - 60')
                                   else:
                                        new_product.discount_percentage = discount_value
                              except:
                                   messages.error(self.request, 'Disocunt value should be number')
                         new_product.save()
                         create_update_product_detail(raw_data, images, new_product, 'create')
          return render(request, self.template_name, self.data)

def create_update_product_detail(raw_data, images, product, operation):
     category_list = raw_data.getlist('category_select', None)
     size_list = raw_data.getlist('size_select', None)
     color_list = raw_data.getlist('color_select', None)
     tag_list = raw_data.getlist('tag_select', None)
     if operation == 'update' and images is not None and len(images) > 0:
          try:
               ProductImages.objects.filter(product=product).delete()
          except:
               pass
     # save images
     if images is not None and len(images) > 0:
          for an_image in images:
               ProductImages(product=product, image=an_image).save()
     # save categorization
     if category_list is not None and len(category_list) > 0 or operation == 'update':
          if operation == 'update':
               try:
                   product.category.clear()
               except:
                   pass
          for category_id in category_list:
               try:
                   category_object = Category.objects.get(id=category_id)
                   product.category.add(category_object)
               except:
                   pass
     
     if size_list is not None and len(size_list) > 0 or operation == 'update':
          if operation == 'update':
               try:
                   product.size.clear()
               except:
                   pass
          for size_id in size_list:
               try:
                   size_object = Size.objects.get(id=size_id)
                   product.size.add(size_object)
               except:
                   pass
     
     if color_list is not None and len(color_list) > 0 or operation == 'update':
          if operation == 'update':
               try:
                   product.color.clear()
               except:
                   pass
          for color_id in color_list:
               try:
                   color_object = Color.objects.get(id=color_id)
                   product.color.add(color_object)
               except:
                   pass
     
     if tag_list is not None and len(tag_list) > 0 or operation == 'update':
          if operation == 'update':
               try:
                   product.tag.clear()
               except:
                   pass
          for tag_id in tag_list:
               try:
                   tag_object = Tag.objects.get(id=tag_id)
                   product.tag.add(tag_object)
               except:
                   pass
     


class AdminUpdateProduct(UpdateView):
     template_name = 'product/admin/admin_update_product.html'
     model = Product
     
     def get(self, request, *args, **kwargs):
          data = {
               'categories': Category.objects.order_by('-id'),
               'colors': Color.objects.order_by('-id'),
               'sizes': Size.objects.order_by('-id'),
               'tags': Tag.objects.order_by('-id'),
               'object': self.get_object(),
          }
          return render(request, self.template_name, data)

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               raw_data = request.POST
               images = request.FILES.getlist('product_images', None)
               print('value of images')
               print(images)
               title = raw_data.get('title', None)
               price = raw_data.get('price', None)
               stock = raw_data.get('stock', None)
               old_price = raw_data.get('old_price', None)
               purchase_price = raw_data.get('purchase_price', None)
               discount_percentage = raw_data.get('discount_percentage', None)
               description = raw_data.get('description', None)
               check_box = raw_data.get('is_active', None)
               is_true = (
                    title is None or title == '' or price is None or price == '' 
                    or stock is None or stock == '' or description is None or description == '' or 
                    purchase_price is None or purchase_price == ''
                    )
               if is_true:
                    messages.error(self.request, "Please fill required fields i.e. title, price, images, stock, and description")
               else:
                    product_obj = self.get_object()
                    if old_price is not None and old_price != '':
                              try:
                                   old_price_value = float(old_price)
                                   product_obj.old_price = old_price_value
                              except:
                                   messages.error(self.request, 'Old price should be digit')
                    if discount_percentage is not None and discount_percentage != '':
                         try:
                              discount_value = int(discount_percentage)
                              if discount_value <= 0 or discount_value > 60:
                                   messages.error(self.request, 'Discount Percentage should be between 1 - 60')
                              else:
                                   product_obj.discount_percentage = discount_value
                         except:
                              messages.error(self.request, 'Disocunt value should be number')
                    try:
                         product_obj.title = title
                         product_obj.active = check_box is not None
                         product_obj.price = float(price)
                         product_obj.purchase_price = float(purchase_price)
                         product_obj.stock = int(stock)
                         product_obj.description = description
                         product_obj.save()
                         if product_obj is not None:
                              create_update_product_detail(raw_data, images, product_obj, 'update')
                    except:
                         messages.error(self.request, 'Uknown Error Occured. Enter your input values correctly')
                         return render(request, self.template_name, {'object': self.get_object()})
          print('shit this part is also executing')
          return redirect('product:admin_product_list')


# List
class AdminCategoryView(ListView):
     template_name = 'product/admin/admin_category_list.html'
     queryset = Category.objects.all().order_by('-id')
     # model = Category
     # queryset = Category.objects.all().order_by('-id')[:5]


class AdminColorView(ListView):
     template_name = 'product/admin/admin_color_list.html'
     queryset = Color.objects.all().order_by('-id')


class AdminSizeView(ListView):
     template_name = 'product/admin/admin_size_list.html'
     queryset = Size.objects.all().order_by('-id')


class AdminTagView(ListView):
     template_name = 'product/admin/admin_tag_list.html'
     queryset = Tag.objects.all().order_by('-id')

# Delete
@login_required
def global_item_deleter(request, *args, **kwargs):
     if request.method == "POST":
          print('valeu of request.POST')
          # newsletter_type
          print(request.POST)
          the_id = request.POST.get('the_id', None)
          operation =  request.POST.get('operation', None)
          if the_id is None or operation is None:
               return JsonResponse({'is_error': True})
          data_dict = {"is_error": False }
          if operation == 'category':
               try:
                   Category.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'size':
               try:
                   Size.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'slider':
               try:
                   Slider.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'newsletter_type':
               try:
                   NewsLetterType.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'shipment':
               try:
                   ShipmentMethod.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'brand':
               try:
                   Brand.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'product':
               try:
                   Product.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'newsletter':
               try:
                   NewsLetter.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'color':
               try:
                   Color.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'tag':
               try:
                   Tag.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'wishlist_item':
               try:
                   WishListItem.objects.get(id=the_id).delete()
               except:
                   data_dict['is_error'] = True
          elif operation == 'cart_item':
               try:
                    CartProduct.objects.get(id=the_id).delete()
                    cart_obj, new_obj = Cart.objects.new_or_get(request)
                    data_dict['subtotal'] = cart_obj.subtotal,
                    data_dict['shipment_fee'] = cart_obj.shipment_fee,
                    data_dict['discount_total'] = cart_obj.discount_total,
                    data_dict['current_item_num'] = cart_obj.current_item_num,
                    data_dict['total'] = cart_obj.total,
               except:
                   data_dict['is_error'] = True
          else:
               data_dict['is_error'] = True
          return JsonResponse(data_dict)

# Create
class AdminCreateCategory(View):
     template_name = 'product/admin/admin_create_category.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               category = request.POST.get('category', None)
               check_box = request.POST.get('is_active', None)
               if category is None or category == '':
                    messages.error(self.request, "Category field is empty")
               else:
                    messages.success(self.request, "Category is saved successfully!")
                    if check_box is None:
                         Category.objects.create(name=category, active=False)
                    else:
                         Category.objects.create(name=category)
          return render(request, self.template_name, {})

class AdminCreateSize(View):
     template_name = 'product/admin/admin_create_size.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               size = request.POST.get('size', None)
               check_box = request.POST.get('is_active', None)
               if size is None or size == '':
                    messages.error(self.request, "Size field is empty")
               else:
                    messages.success(self.request, "Size is saved successfully!")
                    if check_box is None:
                         Size.objects.create(name=size, active=False)
                    else:
                         Size.objects.create(name=size)
          return render(request, self.template_name, {})

class AdminCreateColor(View):
     template_name = 'product/admin/admin_create_color.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               color = request.POST.get('color', None)
               check_box = request.POST.get('is_active', None)
               if color is None or color == '':
                    messages.error(self.request, "Color field is empty")
               else:
                    messages.success(self.request, "Color is saved successfully!")
                    if check_box is None:
                         Color.objects.create(name=color, active=False)
                    else:
                         Color.objects.create(name=color)
          return render(request, self.template_name, {})

class AdminCreateTag(View):
     template_name = 'product/admin/admin_create_tag.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               tag = request.POST.get('tag', None)
               check_box = request.POST.get('is_active', None)
               if tag is None or tag == '':
                    messages.error(self.request, "Tag field is empty")
               else:
                    messages.success(self.request, "Tag is saved successfully!")
                    if check_box is None:
                         Tag.objects.create(name=tag, active=False)
                    else:
                         Tag.objects.create(name=tag)
          return render(request, self.template_name, {})


# Update
class AdminUpdateCategory(UpdateView):
     template_name = 'product/admin/admin_update_category.html'
     model = Category
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               category = request.POST.get('category', None)
               check_box = request.POST.get('is_active', None)
               if category is None or category == '':
                    messages.error(self.request, "Category field is empty")
               else:
                    obj = self.get_object()
                    if check_box is None:
                         obj.name = category
                         obj.active = False
                    else:
                         obj.name = category
                    # SUCCESS
                    obj.save()
                    return redirect('product:admin_category_list')
          return render(request, self.template_name, {'object': self.get_object()})

class AdminUpdateSize(UpdateView):
     template_name = 'product/admin/admin_update_size.html'
     model = Size
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               size = request.POST.get('size', None)
               check_box = request.POST.get('is_active', None)
               if size is None or size == '':
                    messages.error(self.request, "Size field is empty")
               else:
                    obj = self.get_object()
                    if check_box is None:
                         obj.name = size
                         obj.active = False
                    else:
                         obj.name = size
                    # SUCCESS
                    obj.save()
                    return redirect('product:admin_size_list')
          return render(request, self.template_name, {'object': self.get_object()})


class AdminUpdateTag(UpdateView):
     template_name = 'product/admin/admin_update_tag.html'
     model = Tag
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               tag = request.POST.get('tag', None)
               check_box = request.POST.get('is_active', None)
               if tag is None or tag == '':
                    messages.error(self.request, "Tag field is empty")
               else:
                    obj = self.get_object()
                    if check_box is None:
                         obj.name = tag
                         obj.active = False
                    else:
                         obj.name = tag
                    # SUCCESS
                    obj.save()
                    return redirect('product:admin_tag_list')
          return render(request, self.template_name, {'object': self.get_object()})

class AdminUpdateColor(UpdateView):
     template_name = 'product/admin/admin_update_color.html'
     model = Color
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               color = request.POST.get('color', None)
               check_box = request.POST.get('is_active', None)
               if color is None or color == '':
                    messages.error(self.request, "Color field is empty")
               else:
                    obj = self.get_object()
                    if check_box is None:
                         obj.name = color
                         obj.active = False
                    else:
                         obj.name = color
                    # SUCCESS
                    obj.save()
                    return redirect('product:admin_color_list')
          return render(request, self.template_name, {'object': self.get_object()})







