from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register_user, MyOrderListView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'),
         name='login'),
    path('register/', register_user,
         name='register'),
    path('logout/', LogoutView.as_view(),
         name='logout'),
    path('myorders/', MyOrderListView.as_view(),
         name='myorder-list'),
    path('profile/', ProfileView.as_view(),
         name='profile'),
]

app_name = "accounts"