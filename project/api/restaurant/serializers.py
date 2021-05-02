from rest_framework import serializers
from project.feed.models import Restaurant, Offer, Review
from project.feed.models.menu_image import MenuImage
from project.api.reviews.serializers import ReviewSerializer
from django.db.models import Avg
from django.core.exceptions import ObjectDoesNotExist
from project.feed.models.user_coupon import UserCoupon
from datetime import datetime


class RestaurantSerializer(serializers.ModelSerializer):

    reviews = ReviewSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    menu_images = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'country', 'address', 'city', 'zip_code', 'lat', 'long', 'website',
            'phone_number', 'rating', 'email', 'opening_hours', 'price_level', 'category', 'reviews',
            'image', 'logo_image', 'cover_image', 'menu_images', 'is_featured', 'reviews_count']
        read_only_fields = ['id', 'reviews',]

    def get_category(self, restaurant):
        return restaurant.category.name

    def get_reviews_count(self, restaurant):
        return Review.objects.filter(restaurant=restaurant.id).count()
    
    def get_rating(self, restaurant):
        return Review.objects.filter(restaurant=restaurant.id).aggregate(avg_rating=Avg('rating_overall'))
    
    def get_menu_images(self, restaurant):
        menu_images = []
        objs = MenuImage.objects.filter(restaurant__pk=restaurant.pk).order_by('sort_order')
        for obj in objs:
            menu_images.append(obj.image.url)
        return menu_images

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
        fields = ['id', 'name', 'description', 'discounted_price', 'rating', 'original_price', 'restaurant_id', 'image_url',
            'reviews_count', 'valid_from', 'valid_till', 'restaurant_name', 'restaurant_category', 'is_bumper',
            'is_redeemable', 'cover_image', 'can_review'
        ]
        read_only_fields = ['approval_status']

    restaurant_name = serializers.SerializerMethodField()
    restaurant_category = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    cover_image = serializers.SerializerMethodField()
    can_review = serializers.SerializerMethodField()
    is_redeemable = serializers.SerializerMethodField()
    

    def get_restaurant_name(self, offer):
        return offer.restaurant.name
    
    def get_restaurant_category(self, offer):
        return offer.restaurant.category.name
    
    def get_reviews_count(self, offer):
        return Review.objects.filter(offer=offer.id).count()
    
    def get_rating(self, offer):
        return Review.objects.filter(offer=offer.id).aggregate(ave_rating=Avg('rating_overall'))
    
    def get_cover_image(self, offer):
        return offer.restaurant.cover_image.url if offer.restaurant.cover_image else ''
    
    def get_can_review(self, offer):
        try:
            user = self.context.get('request').user
        except:
            user = self.context.user
        if offer.is_bumper:
            return False
        review = Review.objects.filter(
            offer=offer.id,
            restaurant=offer.restaurant,
            user=user
        )
        if review:
            return False
        
        return True
    
    def get_is_redeemable(self, offer):
        try:
            user = self.context.get('request').user
        except:
            user = self.context.user
        today = datetime.now()
        if not offer.is_redeemable or offer.is_bumper:
            return False
        user_coupon = UserCoupon.objects.filter(
            user=user, 
            used_at__year=today.year,
            used_at__month=today.month,
            used_at__day=today.day,
        )
        if user_coupon.filter(coupon__coupon_offer__pk=offer.pk):
            return False
        if user_coupon.count() >= UserCoupon.REDEEM_LIMIT:
            return False
        return True
