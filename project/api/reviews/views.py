from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.base import GetObjectMixin
from project.api.permissions import IsUserOrReadOnly
from project.api.reviews.serializers import ReviewSerializer, TagSerializer
from project.feed.models import Restaurant, Review, ReviewLike, Offer
from project.feed.models.tag import Tag
from django.db.models import Count


class TopReviewsView(GenericAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get(self, request):
        serializer = self.get_serializer(self.queryset.filter().order_by('-rating_overall'), many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class SearchTagsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def post(self, request):
        try: 
            restaurant = Restaurant.objects.get(pk=request.data.get('restaurant_id'))
            if request.data.get('tag'):
                serializer = self.get_serializer(Tag.objects.filter(
                    name__contains=request.data.get('tag'), restaurant=restaurant, is_active=True),
                    many=True
                )
            else:
                 serializer = self.get_serializer(Tag.objects.filter(restaurant=restaurant, is_active=True), many=True)
            if serializer.data:
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                return Response('tag not found')
        except:
            return Response('restaurant not found')


class GetReviewByRestaurantView(GenericAPIView):

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def get(self, request, **kwargs):
        restaurant_id = kwargs.get('restaurant_id')
        review = self.queryset.filter(restaurant=restaurant_id).select_related('restaurant', 'offer', 'user')
        serializer = self.get_serializer(review, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateReview(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def post(self, request):
        data = request.data.dict()
        restaurant = Restaurant.objects.get(pk=int(data.pop('restaurant_id')))
        offer = Offer.objects.get(pk=int(data.pop('offer_id')))

        data['restaurant'] = restaurant
        data['offer'] = offer
        serializer = self.get_serializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid()
        review = serializer.create(data)
        return Response(self.serializer_class(review).data, status.HTTP_201_CREATED)


class AddReviewImage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def post(self, request):
        review = Review.objects.get(pk=int(request.data.get('review_id')))
        review.image = request.data.get('image')
        review.save()
        return Response(self.serializer_class(review).data, status.HTTP_200_OK)
        

class NewReviewView(GetObjectMixin, GenericAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, **kwargs):
        restaurant = self.get_object_by_model(Restaurant, pk=self.kwargs.get('pk'))
        request.restaurant = restaurant
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        new_review = serializer.create(serializer.validated_data)
        return Response(ReviewSerializer(new_review).data, status.HTTP_201_CREATED)


class RestaurantReviewsView(GetObjectMixin, ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def filter_queryset(self, queryset):
        restaurant = self.get_object_by_model(Restaurant, pk=self.kwargs.get('pk'))
        return queryset.filter(restaurant=restaurant).order_by('-created_at')


class UserReviewsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user__username=self.request.user.username)


class ReviewGetUpdateDeleteView(GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsUserOrReadOnly,
    ]

    def get(self, request, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, **kwargs):
        review = self.get_object()
        serializer = self.get_serializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        review = self.get_object()
        review.delete()
        return Response('Deleted')


class LikeUnlikeReviewView(GetObjectMixin, APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, review_id):
        review = self.get_object_by_model(Review, review_id)
        obj, created = ReviewLike.objects.get_or_create(user=request.user, review=review)
        if created:
            return Response(
                {
                    'status_code': 200,
                    'message': 'Review liked!'
                }
            )
        else:
            return Response(
                {
                    'status_code': 422,
                    'message': 'Already liked review.'
                }
            )

    def delete(self, request, review_id):
        review = self.get_object_by_model(Review, review_id)
        try:
            ReviewLike.objects.get(user=request.user, review=review).delete()
            return Response(
                {
                    'status_code': 200,
                    'message': 'Review unliked!'
                }
            )
        except ReviewLike.DoesNotExist:
            return Response(
                {
                    'status_code': 422,
                    'message': 'Invalid review id'
                }
            )


class PopularReviewsView(GenericAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        reviews_like = ReviewLike.objects.values('review__id').annotate(count=Count('review_id')).order_by('-count')
        reviews = []
        for obj in reviews_like:
            review = Review.objects.get(pk=obj.get('review__id'))
            if review.is_active:
                reviews.append(review)
        return Response(ReviewSerializer(reviews, many=True).data, status.HTTP_200_OK)


class LikedReviewsView(GetObjectMixin, APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        reviews = Review.objects.filter(likes__user=request.user)
        return Response(ReviewSerializer(reviews, many=True).data, status.HTTP_200_OK)


class CommentedReviewsView(GetObjectMixin, APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        reviews = Review.objects.filter(comments__user=request.user)
        return Response(ReviewSerializer(reviews, many=True).data, status.HTTP_200_OK)
