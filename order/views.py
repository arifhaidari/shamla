from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView, View, TemplateView
from django.contrib import messages
from django.views.generic.detail import DetailView
from .models import ShipmentMethod, Order


# Completed Order
class AdminCompletedOrderList(ListView):
     template_name = 'order/admin/admin_completed_order_list.html'
     queryset = Order.objects.filter(status=Order.OrderStatus.Shipped).order_by('-id')

# Paid Order
class AdminPaidOrderList(ListView):
     template_name = 'order/admin/admin_paid_order_list.html'
     queryset = Order.objects.filter(status=Order.OrderStatus.Paid).order_by('-id')

# Refunded Order
class AdminRefundedOrderList(ListView):
     template_name = 'order/admin/admin_refunded_order_list.html'
     queryset = Order.objects.filter(status=Order.OrderStatus.Refunded).order_by('-id')


# New Order
class AdminCreatedOrderList(ListView):
     template_name = 'order/admin/admin_new_order_list.html'
     queryset = Order.objects.filter(status=Order.OrderStatus.Created).order_by('-id')


class AdminOrderDetail(DetailView):
     template_name = 'order/admin/admin_order_detail.html'
     model = Order


class OrderReport(TemplateView):
     template_name = 'order/admin/order_report.html'

# Slider
class AdminShipmentList(ListView):
     template_name = 'order/admin/admin_shipment_list.html'
     queryset = ShipmentMethod.objects.all().order_by('-id')

class AdminCreateShipment(View):
     template_name = 'order/admin/admin_shipment_create.html'
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {})
     
     def post(self, request, *args, **kwargs):
          if request.method == 'POST':
               region = request.POST.get('region', None)
               shipment_comment = request.POST.get('shipment_comment', None)
               shipment_fee = request.POST.get('shipment_fee', None)
               free_shipment_limit = request.POST.get('free_shipment_limit', None)
               check_box = request.POST.get('is_active', None)
               if region is None or region == '' or shipment_fee is None or shipment_fee == '':
                    messages.error(self.request, "Enter required fields i.e. region and shipment fee")
               else:
                    is_active = check_box is not None
                    try:
                         the_fee = float(shipment_fee) or 0
                         shipment_object = ShipmentMethod.objects.create(region=region, shipment_fee=the_fee, active=is_active)
                         if shipment_object is not None:
                              if shipment_comment is not None and shipment_comment != '':
                                   shipment_object.shipment_comment = shipment_comment
                              if free_shipment_limit is not None and free_shipment_limit != '':
                                   the_val = float(free_shipment_limit) or 0
                                   shipment_object.free_shipment_limit = the_val
                              shipment_object.save()
                         messages.success(self.request, "Slider data is saved successfully!")
                    except:
                         messages.error(self.request, "Error: Only 25 characters are allowed")
          return render(request, self.template_name, {})


class AdminUpdateShipment(UpdateView):
     template_name = 'order/admin/admin_shipment_update.html'
     model = ShipmentMethod
     
     def get(self, request, *args, **kwargs):
          return render(request, self.template_name, {'object': self.get_object()})

     def post(self, request, *args, **kwargs):
          if request.method == 'POST' and self.get_object() is not None:
               region = request.POST.get('region', None)
               shipment_comment = request.POST.get('shipment_comment', None)
               shipment_fee = request.POST.get('shipment_fee', None)
               free_shipment_limit = request.POST.get('free_shipment_limit', None)
               check_box = request.POST.get('is_active', None)
               if region is None or region == '' or shipment_fee is None or shipment_fee == '':
                    messages.error(self.request, "Enter required fields i.e. region and shipment fee")
               else:
                    try:
                         obj = self.get_object()
                         obj.shipment_fee = float(shipment_fee) or 0
                         obj.region = region
                         if shipment_comment is not None and shipment_comment != '':
                              obj.shipment_comment = shipment_comment
                         if free_shipment_limit is not None and free_shipment_limit != '':
                              the_val = float(free_shipment_limit) or 0
                              obj.free_shipment_limit = the_val
                         obj.active = check_box is not None
                         obj.save()
                         return redirect('order:admin_shipment_list')              
                    except:
                         messages.error(self.request, "Uknown error occured")
          return render(request, self.template_name, {'object': self.get_object()})




