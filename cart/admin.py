from django.contrib import admin


from .models import Cart, CartProduct, WishList, WishListItem

admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(WishList)
admin.site.register(WishListItem)