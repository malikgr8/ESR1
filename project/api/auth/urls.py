from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .views import *
from django.contrib.auth import views

# app_name = 'auth'

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('authenticate', authenticate),
    path('signup', signup),
    path('login', login),
    path('logout', LogoutView.as_view()),
    path('change/password', ChangePassowrdView.as_view()),
    path('forgot/password', ForgotPassowrdView.as_view()),
    path('update/profile', UpdateProfileView.as_view()),
    path('profile', GetProfileView.as_view()),

]
