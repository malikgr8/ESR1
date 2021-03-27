from django.urls import path

from project.api.me.views import (
    GetUpdateUserProfileView, CouponApply,
    GetUserProfileView, UserCouponsView, UserFavOffersView,
    AddUserFavOfferView, GetUserOfferView
)

app_name = 'me'

urlpatterns = [
    path('profile', GetUserProfileView.as_view(), name='profile'),
    path('', GetUpdateUserProfileView.as_view(), name='user_profile'),
    path('coupon/apply', CouponApply.as_view(), name='apply_coupon'),
    path('coupon/all', UserCouponsView.as_view(), name='all_coupons'),
    path('offers', UserFavOffersView.as_view(), name='user_all_offers'),
    path('add/offer', AddUserFavOfferView.as_view(), name='add_user_fav_offer'),
    path('offer/<int:offer_id>', GetUserOfferView.as_view(), name='user_offer_by_id'),

]
