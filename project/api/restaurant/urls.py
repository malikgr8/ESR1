from django.conf.urls import url
from django.urls import path

from project.api.restaurant.views import ListAllRestaurantsView, NewRestaurantView, RestaurantGetUpdateDeleteView, \
    ListCategoryRestaurantsView, UserRestaurantsView, RestaurantImageUploadView, OfferByRestaurant, AllOffers, OfferByName

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
    path('offer_by_name', OfferByName.as_view(), name='offer_by_name'),
]