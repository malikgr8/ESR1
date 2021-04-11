from rest_framework import serializers

from project.feed.models import Review
from project.feed.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name', ]


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    offer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'user', 
            'restaurant_name', 
            'offer_name', 
            'comment', 
            'rating_taste', 
            'rating_ambiance', 
            'rating_quality', 
            'rating_money_value', 
            'updated_at',
            'rating_overall',
            'image',
            'tags'
        ]

    def create(self, validated_data):
        post_data = self.context.get('request').data
        post_data = validated_data
        rating_list = [
            int(post_data.get('rating_taste')),
            int(post_data.get('rating_ambiance')),
            int(post_data.get('rating_quality')),
            int(post_data.get('rating_money_value'))
        ]
        rating_overall = sum(rating_list) / len(rating_list)
        return Review.objects.create(
            user=self.context.get('request').user,
            restaurant=post_data.get('restaurant'),
            offer=post_data.get('offer'),
            comment=post_data.get('comment'),
            rating_taste=int(post_data.get('rating_taste')),
            rating_ambiance=int(post_data.get('rating_ambiance')),
            rating_quality=int(post_data.get('rating_quality')),
            rating_money_value=int(post_data.get('rating_money_value')),
            rating_overall=rating_overall,
            tags=post_data.get('tags'),
            image=post_data.get('image', '')
        )
    
    def get_user(self, review):
        return "{} {}".format(review.user.first_name, review.user.last_name) 
    
    def get_offer_name(self, review):
        return review.offer.name
    
    def get_restaurant_name(self, review):
        return review.restaurant.name