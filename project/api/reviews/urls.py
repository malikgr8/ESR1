from django.urls import path

from project.api.reviews.views import NewReviewView, RestaurantReviewsView, UserReviewsView, ReviewGetUpdateDeleteView, \
    LikeUnlikeReviewView, LikedReviewsView, CommentedReviewsView, GetReviewByRestaurantView, CreateReview, AddReviewImage

app_name = 'reviews'

urlpatterns = [
    path('restaurant/<int:restaurant_id>', GetReviewByRestaurantView.as_view(), name='get_reviews_by_restaurant'),
    path('post', CreateReview.as_view(), name='create_review'),
    path('post/image', AddReviewImage.as_view(), name='create_review'),



    path('new_review/<int:pk>/', NewReviewView.as_view(), name='new_review'),
    path('restaurant/<int:pk>/', RestaurantReviewsView.as_view(), name='restaurant_reviews'),
    path('user/<int:pk>/', UserReviewsView.as_view(), name='user_reviews'),
    # path('<int:pk>/', ReviewGetUpdateDeleteView.as_view(), name='review_get_update_delete'),
    path('like/<int:review_id>/', LikeUnlikeReviewView.as_view(), name='like_unlike_review'),
    path('likes/', LikedReviewsView.as_view(), name='liked_reviews'),
    path('comments/', CommentedReviewsView.as_view(), name='commented_reviews'),
]
