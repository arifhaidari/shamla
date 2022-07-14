from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .admin_views import (
    AdminProductView, AdminCategoryView, AdminColorView, AdminSizeView, AdminTagView, 
    AdminCreateCategory, AdminUpdateCategory, AdminCreateColor, AdminCreateSize, AdminCreateTag, AdminUpdateColor,
    AdminUpdateSize, AdminUpdateTag, global_item_deleter, AdminProductDetail, AdminCreateProduct,
    AdminUpdateProduct
    )

from .views import ProductDetailView, ProductListView

app_name = 'product'

urlpatterns = [
    # ===============Public====================
    path('list/', ProductListView.as_view(), name="product_list"),
    path('detail/<slug>/', ProductDetailView.as_view(), name="product_detail"),
    
    # ===============Public user====================
    
    # ===============Admin====================
    # product
    path('admin/product/list/', staff_member_required(AdminProductView.as_view()), name="admin_product_list"),
    path('admin/product/create/', staff_member_required(AdminCreateProduct.as_view()), name="admin_product_create"),
    path('admin/product/detail/<slug>/', staff_member_required(AdminProductDetail.as_view()), name="admin_product_detail"),
    path('admin/product/update/<slug>/', staff_member_required(AdminUpdateProduct.as_view()), name="admin_product_update"),
    # ===========SEO Start============
    # list
    path('admin/category/list/', staff_member_required(AdminCategoryView.as_view()), name="admin_category_list"),
    path('admin/color/list/', staff_member_required(AdminColorView.as_view()), name="admin_color_list"),
    path('admin/size/list/', staff_member_required(AdminSizeView.as_view()), name="admin_size_list"),
    path('admin/tag/list/', staff_member_required(AdminTagView.as_view()), name="admin_tag_list"),
    # create
    path('admin/category/create/', staff_member_required(AdminCreateCategory.as_view()), name="admin_category_create"),
    path('admin/color/create/', staff_member_required(AdminCreateColor.as_view()), name="admin_color_create"),
    path('admin/size/create/', staff_member_required(AdminCreateSize.as_view()), name="admin_size_create"),
    path('admin/tag/create/', staff_member_required(AdminCreateTag.as_view()), name="admin_tag_create"),
    # update
    path('admin/category/update/<pk>/', staff_member_required(AdminUpdateCategory.as_view()), name="admin_category_update"),
    path('admin/color/update/<pk>/', staff_member_required(AdminUpdateColor.as_view()), name="admin_color_update"),
    path('admin/size/update/<pk>/', staff_member_required(AdminUpdateSize.as_view()), name="admin_size_update"),
    path('admin/tag/update/<pk>/', staff_member_required(AdminUpdateTag.as_view()), name="admin_tag_update"),
    # ===========SEO End============
    
    # delete
    path('admin/delete/item/', global_item_deleter, name="delete_seo_item"),
    
    # ===============Normal User====================
    
]

