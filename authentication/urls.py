from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("login/", Login, name="admin_login"),
    path("logout/", LogoutUser, name="admin_logout"),
    path("sign-up/", newusers, name="admin_new_users"),
]
