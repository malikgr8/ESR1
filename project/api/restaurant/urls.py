from django.conf.urls import url
from django.urls import path

from project.api.restaurant.views import (
    ListAllRestaurantsView, NewRestaurantView, RestaurantGetUpdateDeleteView,
    TopRatedRestaurantsView, TopRated4RestaurantsView,
    ListCategoryRestaurantsView, UserRestaurantsView, RestaurantImageUploadView,
     OfferByRestaurant, AllOffers, OfferById, BumperOffers, AllTopOffers
)

from project.api.restaurant import views

app_name = 'restaurants'

urlpatterns = [
    path('', ListAllRestaurantsView.as_view(), name='all'),
    path('?search=<str:search_string>', ListAllRestaurantsView.as_view(), name='search_restaurant'),
    path('new/', NewRestaurantView.as_view(), name='new_restaurant'),
    path('img_upload/', RestaurantImageUploadView.as_view(), name='restaurant_image_upload'),
    path('user/<int:pk>/', UserRestaurantsView.as_view(), name='user_restaurants'),
    path('category/<int:pk>/', ListCategoryRestaurantsView.as_view(), name='category_restaurants'),
    path('<int:pk>/', RestaurantGetUpdateDeleteView.as_view(), name='get_update_delete_restaurant'),
    path('<int:restaurant_id>/offer', OfferByRestaurant.as_view(), name='offer_by_restaurant'),
    path('offers', AllOffers.as_view(), name='all_offers'),
    path('offers/bumper', BumperOffers.as_view(), name='all_offers'),
    path('offer/<int:id>', OfferById.as_view(), name='offer_by_id'),
    path('top4', TopRated4RestaurantsView.as_view(), name='top_rated_4_restaurants'),
    path('top/all', TopRatedRestaurantsView.as_view(), name='top_rated_restaurants'),
    path('top/offers', AllTopOffers.as_view(), name='top_rated_offers'),

]