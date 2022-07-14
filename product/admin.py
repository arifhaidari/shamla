from django.contrib import admin

from .models import Product, Color, Size, Category, Tag, ProductImages


admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ProductImages)