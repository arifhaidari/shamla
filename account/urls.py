from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .views import RegisterView, LoginView, UserProfile, AdminUerList, AdminUserDetail

app_name = 'account'

urlpatterns = [
    # Admin part
    path('list/', staff_member_required(AdminUerList.as_view()), name="user_list"),
    path('detail/<int:pk>', staff_member_required(AdminUserDetail.as_view()), name="user_detail"),
    # public part
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('profile/', login_required(UserProfile.as_view()), name="profile"),
]