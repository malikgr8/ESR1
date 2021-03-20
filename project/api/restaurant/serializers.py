from rest_framework import serializers
from project.feed.models import Restaurant, Offer, Review
from project.api.reviews.serializers import ReviewSerializer
from django.db.models import Avg

class RestaurantSerializer(serializers.ModelSerializer):


    reviews = ReviewSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'country', 'street', 'city', 'zip', 'website', 'phone_number', 'rating',
                  'email', 'opening_hours', 'price_level', 'category', 'user', 'reviews', 'image', 'reviews_count']
        read_only_fields = ['id', 'user', 'reviews',]

    def get_category(self, restaurant):
        return restaurant.category.name

    def get_reviews_count(self, restaurant):
        return Review.objects.filter(restaurant=restaurant.id).count()
    
    def get_rating(self, restaurant):
        return Review.objects.filter(restaurant=restaurant.id).aggregate(ave_rating=Avg('rating_overall'))

    def create(self, validated_data):
        return Restaurant.objects.create(
            **validated_data,
            user=self.context.get('request').user
        )


class RestaurantImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['image']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'name', 'discounted_price', 'rating',
                  'original_price', 'restaurant_id', 'image_url', 'reviews_count',
                  'valid_from', 'valid_till', 'restaurant_name', 'restaurant_category'
                  ]
        read_only_fields = ['approval_status']

    restaurant_name = serializers.SerializerMethodField()
    restaurant_category = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    

    def get_restaurant_name(self, offer):
        return offer.restaurant.name
    
    def get_restaurant_category(self, offer):
        return offer.restaurant.category.name
    
    def get_reviews_count(self, offer):
        return Review.objects.filter(offer=offer.id).count()
    
    def get_rating(self, offer):
        return Review.objects.filter(offer=offer.id).aggregate(ave_rating=Avg('rating_overall'))
    
    