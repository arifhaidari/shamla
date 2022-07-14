from django.urls import path, include


from .views import (
     AdminCreateShipment, AdminShipmentList, AdminUpdateShipment, OrderReport, 
     AdminCompletedOrderList, AdminCreatedOrderList, AdminPaidOrderList, AdminRefundedOrderList, 
     AdminOrderDetail
     )

app_name = 'order'

urlpatterns = [
    path('admin/report/', OrderReport.as_view(), name="admin_report_list"),
    path('admin/new/', AdminCreatedOrderList.as_view(), name="admin_new_list"),
    path('admin/completed/', AdminCompletedOrderList.as_view(), name="admin_completed_list"),
    path('admin/paid/', AdminPaidOrderList.as_view(), name="admin_paid_list"),
    path('admin/refunded/', AdminRefundedOrderList.as_view(), name="admin_refunded_list"),
    path('admin/shipment/list/', AdminShipmentList.as_view(), name="admin_shipment_list"),
    path('admin/order/<int:pk>/', AdminOrderDetail.as_view(), name="admin_order_detail"),
    path('admin/shipment/update/<pk>/', AdminUpdateShipment.as_view(), name="admin_shipment_update"),
    path('admin/shipment/create/', AdminCreateShipment.as_view(), name="admin_shipment_create"),
]