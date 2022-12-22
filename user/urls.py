from django.urls import path

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from user import views

app_name = 'user'

urlpatterns = [
    path("", views.CreateUserView.as_view(), name="user_create"),
    # path("token", TokenObtainPairView.as_view(), name="get_token"),
    path("token", views.ObtainPairTokenView.as_view(), name="get_token"),
    path("token/refresh", TokenRefreshView.as_view(), name="refresh_token"),
]
