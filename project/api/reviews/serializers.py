from rest_framework import serializers

from project.feed.models import Review


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    restaurant = serializers.SerializerMethodField()
    offer = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['user', 'restaurant', 'offer', 'comment', 'rating', 'updated_at']

    def create(self, validated_data):
        post_data = self.context.get('request').data
        return Review.objects.create(
            user=self.context.get('request').user,
            restaurant=post_data.get('restaurant'),
            offer=post_data.get('offer'),
            comment=post_data.get('comment'),
            rating=post_data.get('rating')
        )
    
    def get_user(self, review):
        return "{} {}".format(review.user.first_name, review.user.last_name) 
    
    def get_offer(self, review):
        return review.offer.name
    
    def get_restaurant(self, review):
        return review.restaurant.name