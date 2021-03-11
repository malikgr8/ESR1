from rest_framework import serializers
from project.feed.models import Restaurant, Offer
from project.api.reviews.serializers import ReviewSerializer

class RestaurantSerializer(serializers.ModelSerializer):


    reviews = ReviewSerializer(read_only=True, many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'country', 'street', 'city', 'zip', 'website', 'phone_number',
                  'email', 'opening_hours', 'price_level', 'category', 'user', 'reviews', 'image']
        read_only_fields = ['id', 'user', 'reviews']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     return {
    #         **data,
    #         'restaurants_count': instance.restaurants.count(),
    #     }

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
        fields = ['id', 'name', 'discounted_price',
                  'original_price', 'restaurant_id', 'image_url',
                  'valid_from', 'valid_till',
                  ]
        read_only_fields = ['approval_status']