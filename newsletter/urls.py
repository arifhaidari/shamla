from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .views import (MailingListView, NewsletterTypeView, NewsletterView, NewsletterTypeCreateView, 
                    NewsletterTypeUpdateView, NewsletterCreateView, NewsletterUpdateView, 
                    CustomerMessageListView)

app_name = 'newsletter'

urlpatterns = [
    # =================== Admin ======================
    path('admin/type/', staff_member_required(NewsletterTypeView.as_view()), name="newsletter_type_list"),
    path('admin/mailing/list/', staff_member_required(MailingListView.as_view()), name="mailing_list"),
    path('admin/list/', staff_member_required(NewsletterView.as_view()), name="newsletter_list"),
    path('admin/type/create/', staff_member_required(NewsletterTypeCreateView.as_view()), name="newsletter_type_create"),
    path('admin/type/<int:pk>/', staff_member_required(NewsletterTypeUpdateView.as_view()), name="newsletter_type_update"),
    path('admin/create/', staff_member_required(NewsletterCreateView.as_view()), name="newsletter_create"),
    path('admin/<int:pk>/', staff_member_required(NewsletterUpdateView.as_view()), name="newsletter_update"),
    path('admin/message/list/', staff_member_required(CustomerMessageListView.as_view()), name="customer_message_list"),
]

