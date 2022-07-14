from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # change password
    path('password/change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # reset password
    # path('accounts/', include('django.contrib.auth.urls')),
    path("password_reset/", auth_views.PasswordResetView.as_view(),
         name="password_reset"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
