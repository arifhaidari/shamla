"""shamla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from .views import HomePage, About, Contact, WishItemList, update_wish_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(),  name='home'),
    path('logout/', LogoutView.as_view(),  name='logout'),
    path('about/', About.as_view(),  name='about'),
    path('contact/', Contact.as_view(),  name='contact'),
    path('wishlist/', login_required(WishItemList.as_view()),  name='wishlist'),
    path('wishlist/update/', update_wish_list,  name='update_wish_list'),
    # Apps
    path('credential/', include("account.credential_management.urls")),
    path('account/', include('account.urls', namespace='account')),
    path('address/', include('address.urls', namespace='address')),
    path('analytic/', include('analytic.urls', namespace='analytic')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('marketing/', include('marketing.urls', namespace='marketing')),
    path('order/', include('order.urls', namespace='order')),
    path('product/', include('product.urls', namespace='product')),
    path('search/', include('search.urls', namespace='search')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('newsletter/', include('newsletter.urls', namespace='newsletter')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

