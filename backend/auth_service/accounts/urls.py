# auth_service/urls.py
from django.urls import path

from accounts.views import RegisterView, LoginView, RefreshTokenView, UserView, LogoutView, VerifyTokenView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('refresh', RefreshTokenView.as_view(), name='refresh'),
    path('user', UserView.as_view(), name='user'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token')
]
