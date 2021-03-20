from rest_framework import serializers

from project.feed.models import Review
from project.feed.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name', ]


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    review_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = [
            'review_id',
            'user', 
            'restaurant', 
            'offer', 
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
        rating_list = [
            post_data.get('rating_taste'),
            post_data.get('rating_ambiance'),
            post_data.get('rating_quality'),
            post_data.get('rating_money_value')
        ]
        rating_overall = sum(rating_list) / len(rating_list)
        return Review.objects.create(
            user=self.context.get('request').user,
            restaurant=post_data.get('restaurant'),
            offer=post_data.get('offer'),
            comment=post_data.get('comment'),
            rating_taste=post_data.get('rating_taste'),
            rating_ambiance=post_data.get('rating_ambiance'),
            rating_quality=post_data.get('rating_quality'),
            rating_money_value=post_data.get('rating_money_value'),
            rating_overall=rating_overall,
            tags=post_data.get('tags')
        )

    def get_review_id(self, review):
        return review.id

    def get_user(self, review):
        return "{} {}".format(review.user.first_name, review.user.last_name) 
    
    def get_offer(self, review):
        return review.offer.name
    
    def get_restaurant(self, review):
        return review.restaurant.name