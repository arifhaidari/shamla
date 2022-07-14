from django.urls import path, include
from .views import (CreateCheckoutSessionView, stripe_webhook, OrderSummary)
from django.contrib.auth.decorators import login_required

app_name = 'billing'

urlpatterns = [
    path('payment-method/', login_required(CreateCheckoutSessionView.as_view()), name="payment_method"),
    path('webhook/', stripe_webhook, name="webhook"),
    path('summary/<order_id>/', login_required(OrderSummary.as_view()), name="order_summary"),
    # path('payment-method/', payment_method_view, name="register"),
]