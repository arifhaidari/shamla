import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import message, send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import View, TemplateView
from django.urls import reverse, reverse_lazy
# from django.contrib.auth.decorators import login_required

User = get_user_model()

import stripe

from cart.models import Cart
from order.models import Order
from shamla.views import get_cart_brief_items
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_kelVPmtJ1IDnXDF3oaQGq4JL000WOFQ3tY")
STRIPE_PUB_KEY =  getattr(settings, "STRIPE_PUB_KEY", 'pk_test_b7mDswFCelSp7EKwyFuoSK5Z00dboIClCl')
WEBHOOK_SECRET_KEY =  getattr(settings, "WEBHOOK_SECRET_KEY", 'whsec_2Z6xXHhNcGTG2G9wRhvzWcVAetajWPdB')
stripe.api_key = STRIPE_SECRET_KEY


from .models import BillingProfile, Card, Charge



class OrderSummary(View):
     template_name = 'billing/order_summary.html'
     
     def get(self, request , *args, **kwargs):
          is_error = False
          order_object = None
          print('value of kwargs')
          print(kwargs)
          order_id = kwargs['order_id']
          try:
               order_object = Order.objects.get(order_id=order_id)
          except:
               messages.error(request, 'Unknown Error Occured. Please try again')
               is_error = True
          cart_data = get_cart_brief_items(request)
          the_data = {
               'cart_data': cart_data,
               'order_object': order_object,
          }
          return render(request, self.template_name, the_data) if not is_error else redirect('cart:item_list')
     

class CreateCheckoutSessionView(View):
     
     def post(self, request, *args, **kwargs):
          cart_obj, new_obj = Cart.objects.new_or_get(request)
          try:
               order_queryset = Order.objects.filter(cart=cart_obj, active=True, status=Order.OrderStatus.Created).order_by('-id', '-updated')
               order_object = order_queryset.first()
               the_price = int(cart_obj.total * 100)
          except:
               messages.error(request, 'There is no order created. Please try again')
               return redirect('cart:checkout')
          YOUR_DOMAIN = 'http://127.0.0.1:8000'
          print('value of request ------')
          # print(request.POST.get(''))
          user = request.user or "Uknown User"
          product = stripe.Product.create(
               name = order_object.order_id,
               description=f'This Order was placed on {order_object.updated} by {user}'
               )
          # attach the customer id somewhere in order 
          # check is there any alternative for product to show order data instead of product or just make a work around 
          
          price = stripe.Price.create(
          product= product.id,
          unit_amount=the_price, # it is 20 usd
          currency='usd',
          )
          try:
               checkout_session = stripe.checkout.Session.create(
                    line_items=[
                         {
                              'price': price.id,
                              'quantity': 1,
                         },
                    ],
                    payment_method_types=[
                    'card',
                    ],
                    mode='payment',
                    # by metadata in webhook i can access this data to send it by email
                    metadata = {
                         'order_id': order_object.order_id,
                         'user_id': user.id,
                         'cart_id': cart_obj.id,
                    },
                    success_url=YOUR_DOMAIN,
                    cancel_url=YOUR_DOMAIN + f'/billing/summary/{order_object.order_id}/',
               )
               print('value of checkout_session.url')
               print(checkout_session)
          except Exception as e:
               print('value of str(e)')
               print(str(e))
               return HttpResponse(str(e))
          # return JsonResponse({'id': checkout_session.id})
          return redirect(checkout_session.url, status_code=303)


# @login_required
@csrf_exempt
def stripe_webhook(request):
     print('value of request++++++++++++++')
     print('inside the stripe_webhook')
     print('value of request.user ')
     print(request.user)
     payload = request.body
     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
     event = None

     try:
          event = stripe.Webhook.construct_event(
               payload, sig_header, WEBHOOK_SECRET_KEY
          )
     except ValueError as e:
          # Invalid payload
          print('Invalid payload')
          return HttpResponse(status=400)
     except stripe.error.SignatureVerificationError as e:
          # Invalid signature
          print('Invalid signature')
          return HttpResponse(status=400)
     
     if event['type'] == 'checkout.session.completed':
          session = event['data']['object']
          # this come after charge.succeeded
          fulfill_order(request, session)
     # print('value of event')
     # print(event)
     if event['type'] == 'charge.succeeded':
          print('it is charge.succeeded ====')
          print(event)
          print('/////////')
          save_the_charge(event)
          
     # if event['type'] == 'payment_intent.payment_failed':
     # print(event['data']['object']['charges']['data'][0]['failure_message'])
     # if event['type'] == 'charge.failed':
     # maybe add any action
     return HttpResponse(status=200)

def save_the_charge(event):
     if event['data']['object']['paid']: # boolean
          card_obj = Card.objects.create(
               # billing_profile = billing_profile, # add it in session completion
               payment_intent = event['data']['object']['payment_intent'],
               brand = event['data']['object']['payment_method_details']['card']['brand'],
               country = event['data']['object']['payment_method_details']['card']['country'],
               exp_month = event['data']['object']['payment_method_details']['card']['exp_month'],
               exp_year = event['data']['object']['payment_method_details']['card']['exp_year'],
               last4 = event['data']['object']['payment_method_details']['card']['last4'],
          )
          # save Charge
          Charge.objects.create(
               card = card_obj,
               charge_id = event['data']['object']['id'],
               fingerprint = event['data']['object']['payment_method_details']['card']['fingerprint'],
               paid = event['data']['object']['paid'],
               outcome_type = event['data']['object']['outcome']['type'],
               seller_message = event['data']['object']['outcome']['seller_message'],
               risk_level = event['data']['object']['outcome']['risk_level'],
               risk_score = event['data']['object']['outcome']['risk_score'],
          )
          
          pass
     pass

def fulfill_order(request, session):
     print('value of session')
     print(session)
     customer_email = session['customer_details']['email']
     order_id = session['metadata']['order_id']
     user_id = session['metadata']['user_id']
     cart_id = session['metadata']['cart_id']
     try:
          user = User.objects.get(id=user_id)
          print('value of user ===== ')
          print(user)
     except:
          print('error in accessing the user')
          user = None
     if session['payment_status'] == 'paid':
          try:
               cart_obj, new_obj = Cart.objects.new_or_get(request, cart_id)
               order_obj = Order.objects.get(order_id=order_id, cart=cart_obj)
               cart_obj.is_checked_out = True
               cart_obj.save()
               order_obj.status=Order.OrderStatus.Paid
               order_obj.save()
               send_mail(
                    subject='You have ordered successfully',
                    message=f'You have ordered successfully and your order id is {order_id}',
                    recipient_list=[customer_email],
                    from_email= 'random@gmail.com'
               )
          except:
               pass
     billing_profile = user.billingprofile
     # cart_obj, new_obj = Cart.objects.new_or_get(request, cart_id, user)
     try:
          print('value of paymnt intent')
          print(session['payment_intent'])
          card = Card.objects.get(payment_intent=session['payment_intent'])
          card.billing_profile = billing_profile
          card.save()
     except:
          pass
     




