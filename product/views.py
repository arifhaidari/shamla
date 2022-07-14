from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DetailView, DeleteView
from django.views.generic.dates import timezone_today
from cart.models import Cart
from marketing.models import Slider, Brand
from django.db.models import Q

from shamla.views import get_cart_brief_items
from .models import Product, Category, ProductImages, Size, Color, Tag
from django.core.paginator import EmptyPage, Paginator
import itertools

class ProductListView(ListView):
     template_name = 'product/product_list.html'
     model = Product
     paginate_by = 5
     # queryset = Product.objects.order_by('-id')
     
     def get_context_data(self, *args, **kwargs):
          context = super().get_context_data(**kwargs)
          query = self.request.GET.get('q', None)
          # cart_obj, new_obj = Cart.objects.new_or_get(self.request)
          # print(cart_obj.current_item_num)
          # self.request.session['cart_items'] = cart_obj.current_item_num
          if query is not None and query != '' and query != '0':
               try:
                    category_id = int(query)
                    category_object = Category.objects.get(id=category_id)
                    context['object_list'] = Product.objects.filter(category__id=category_id).order_by('-id')
                    context['category'] = category_object.name
                    print('it is integer')
               except:
                    print('it is not id')
                    context['category'] = 'All Products'
                    if query == 'a_to_z':
                         context['object_list'] = Product.objects.order_by('title')
                    elif query == 'z_to_a':
                         context['object_list'] = Product.objects.order_by('-title')
                    elif query == 'low_to_high':
                         context['object_list'] = Product.objects.order_by('price')
                    elif query == 'high_to_low':
                         context['object_list'] = Product.objects.order_by('-price')
                    else:
                         # all
                         context['object_list'] = Product.objects.all()
          else:
               context['category'] = 'All Products'
          context['categories'] = Category.objects.order_by('-id')
          context['cart_data'] = get_cart_brief_items(self.request)
          return context


class ProductDetailView(DetailView):
     model = Product
     template_name = 'product/product_detail.html'
     
     # def get_object(self, )
     
     def get_context_data(self, **kwargs):
          print('value of kwargs')
          # product_object = kwargs['object']
          context = super().get_context_data(**kwargs)
          product_object = kwargs['object']
          context['cart_data'] = get_cart_brief_items(self.request)
          context['related_products'] = None
          try:
              frist_category = product_object.category.first() or None
              last_category = product_object.category.last() or None
              if frist_category is not None and last_category is not None:
                   first_related = Product.objects.filter(category=frist_category).exclude(id=product_object.id).order_by('-id')[:5]
                   second_rlateed = Product.objects.filter(category=last_category).exclude(id=product_object.id).order_by('-id')[:5]
                   context['related_products'] = list(itertools.chain(first_related, second_rlateed))
              elif frist_category is not None:
                   print('i am in the frist_category is None')
                   context['related_products'] = Product.objects.filter(category=frist_category).exclude(id=product_object.id).order_by('-id')[:10]
              else:
                   print('i ma in the else')
                   context['related_products'] = Product.objects.all().exclude(id=product_object.id).order_by('-id')[:10]
                   
                   
          except:
              pass
          return context








