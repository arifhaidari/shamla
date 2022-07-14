from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .admin_views import (
    AdminCreateSlider, AdminSliderListView, AdminUpdateSlider, 
    AdminBrandListView, AdminCreateBrand, AdminUpdateBrand, 
    AdminCoolCustomerListView, AdminCreateCoolCustomer, AdminUpdateCoolCustomer, 
    AdminSpecialOfferListView, AdminCreateSpecialOffer, AdminUpdateSpecialOffer, 
    ManageRecommendation
    )

app_name = 'marketing'

urlpatterns = [
    # =================== public user ======================
    # =================== Admin ======================
    path('admin/recommend/', staff_member_required(ManageRecommendation.as_view()), name="home_recommendation"),
    # Slider
    path('admin/slider/list', staff_member_required(AdminSliderListView.as_view()), name="admin_slider_list"),
    path('admin/slider/create', staff_member_required(AdminCreateSlider.as_view()), name="admin_slider_create"),
    path('admin/slider/update/<pk>/', staff_member_required(AdminUpdateSlider.as_view()), name="admin_slider_update"),
    # Brand
    path('admin/brand/list', staff_member_required(AdminBrandListView.as_view()), name="admin_brand_list"),
    path('admin/brand/create', staff_member_required(AdminCreateBrand.as_view()), name="admin_brand_create"),
    path('admin/brand/update/<pk>/', staff_member_required(AdminUpdateBrand.as_view()), name="admin_brand_update"),
    # Cool Customer Discount
    path('admin/cool/list', staff_member_required(AdminCoolCustomerListView.as_view()), name="admin_cool_list"),
    path('admin/cool/create', staff_member_required(AdminCreateCoolCustomer.as_view()), name="admin_cool_create"),
    path('admin/cool/update/<pk>/', staff_member_required(AdminUpdateCoolCustomer.as_view()), name="admin_cool_update"),
    # Special Offer Discount
    path('admin/special/list', staff_member_required(AdminSpecialOfferListView.as_view()), name="admin_special_list"),
    path('admin/special/create', staff_member_required(AdminCreateSpecialOffer.as_view()), name="admin_special_create"),
    path('admin/special/update/<pk>/', staff_member_required(AdminUpdateSpecialOffer.as_view()), name="admin_special_update"),
]