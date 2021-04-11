from django.conf.urls import url
from django.urls import path

from project.api.restaurant.views import (
    NewRestaurantView, RestaurantGetUpdateDeleteView,
    TopRatedRestaurantsView, TopRated4RestaurantsView,
    ListCategoryRestaurantsView, RestaurantImageUploadView,
    OfferByRestaurant, AllOffers, OfferById, BumperOffers, AllTopOffers,
    ListAllRestaurantsView
)

from project.api.restaurant import views

app_name = 'restaurants'

urlpatterns = [
    # restaurant related routes
    path('<int:pk>/', RestaurantGetUpdateDeleteView.as_view(), name='get_update_delete_restaurant'),
    path('', ListAllRestaurantsView.as_view(), name='all'),
    path('<int:restaurant_id>/offers', OfferByRestaurant.as_view(), name='offer_by_restaurant'),
    path('?search=<str:search_string>', ListAllRestaurantsView.as_view(), name='search_restaurant_offers'),
    # top avg rating of reviews based restraurants
    path('top/all', TopRatedRestaurantsView.as_view(), name='top_rated_restaurants'),
    # category based restaurants
    path('category/<int:pk>/', ListCategoryRestaurantsView.as_view(), name='category_restaurants'),


    # offers related routes
    path('offer/<int:id>', OfferById.as_view(), name='offer_by_id'),
    path('offers', AllOffers.as_view(), name='all_offers'),
    path('offers/bumper', BumperOffers.as_view(), name='all_bumper_offers'),
    

    
   


    path('top/offers', AllTopOffers.as_view(), name='top_rated_offers'),
    path('top4', TopRated4RestaurantsView.as_view(), name='top_rated_4_restaurants'),
    path('new/', NewRestaurantView.as_view(), name='new_restaurant'),
    path('img_upload/', RestaurantImageUploadView.as_view(), name='restaurant_image_upload'),
    
    

]