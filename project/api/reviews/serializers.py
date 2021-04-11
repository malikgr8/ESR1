from rest_framework import serializers

from project.feed.models import Review
from project.feed.models.reveiw_images import ReviewImage
from project.feed.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name', ]


class ReviewSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    restaurant_name = serializers.SerializerMethodField()
    offer_name = serializers.SerializerMethodField()
    review_images = serializers.SerializerMethodField()
    
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
            'tags',
            'review_images'
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
        review = Review.objects.create(
            user=self.context.get('request').user,
            restaurant=post_data.get('restaurant'),
            offer=post_data.get('offer'),
            comment=post_data.get('comment'),
            rating_taste=int(post_data.get('rating_taste')),
            rating_ambiance=int(post_data.get('rating_ambiance')),
            rating_quality=int(post_data.get('rating_quality')),
            rating_money_value=int(post_data.get('rating_money_value')),
            rating_overall=rating_overall,
            tags=post_data.get('tags')
        )
        image_list = []
        if post_data.get('image_1'):
            image_list.append(post_data.get('image_1'))
        if post_data.get('image_2'):
            image_list.append(post_data.get('image_2'))
        if post_data.get('image_3'):
            image_list.append(post_data.get('image_3'))
        if post_data.get('image_4'):
            image_list.append(post_data.get('image_4'))
        if post_data.get('image_5'):
            image_list.append(post_data.get('image_5'))
        for image in image_list:
            ReviewImage.objects.create(
                image_url=image,
                review=review
            )
        return review

    
    def get_user(self, review):
        return "{} {}".format(review.user.first_name, review.user.last_name) 
    
    def get_offer_name(self, review):
        return review.offer.name
    
    def get_restaurant_name(self, review):
        return review.restaurant.name
    
    def get_review_images(self, review):
        reveiw_images = []
        objs = ReviewImage.objects.filter(review__pk=review.pk)
        for image in objs:
            reveiw_images.append(image.image_url.url)
        return reveiw_images


class ReviewImageSerializer(serializers.ModelSerializer):

        class Meta:
            model = ReviewImage
            fields = ['image_url'] 