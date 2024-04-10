from . import views_auth
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,  TokenVerifyView)
urlpatterns = [ 
    path("signup/",views_auth.SignUpView.as_view(),name="signup"),
    path("login/",views_auth.LoginView.as_view(),name="login"),
    path("jwt/create/",TokenObtainPairView.as_view(),name="jwt_create"), #Este quedo como login
    path("jwt/refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path("jwt/verify/",TokenVerifyView.as_view(),name="token_verify"),
]