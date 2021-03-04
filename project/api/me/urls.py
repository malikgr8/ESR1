from django.urls import path

from project.api.me.views import GetUpdateUserProfileView, use_Coupon

app_name = 'me'

urlpatterns = [
    path('', GetUpdateUserProfileView.as_view(), name='user_profile'),
    path('usecoupon', use_Coupon)
]
