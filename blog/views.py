from django.shortcuts import render
from django.views.generic import View, ListView

from shamla.views import get_cart_brief_items


class BlogList(View):
     template_name = 'blog/blog_list.html'
     
     def get(self, request, *args, **kwargs):
          the_data = {
               'cart_data': get_cart_brief_items(request),
          }
          return render(request, self.template_name, the_data)
