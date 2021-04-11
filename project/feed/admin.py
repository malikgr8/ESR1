from django.contrib import admin
#from django_simple_coupons.models import Coupon

from project.feed.models import Restaurant, Review, Comment, Profile, Category, ReviewLike, CommentLike

from project.feed.models import Offer
from .models import coupon
from .models.coupon import Coupon
from .models.user_coupon import UserCoupon
from .models.user_offers import UserOffers
from project.feed.models.admin_ad import AdminAd
from project.feed.models.tag import Tag


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'phone_number', 'email', 'opening_hours', 'country', 'address', 'city',
        'zip_code', 'lat', 'long', 'price_level', 'image', 'logo_image', 'cover_image', 'menu_image', 'is_featured'
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'content']


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone_number', 'things_love', 'description']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'review']


class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']


class OfferAdmin(admin.ModelAdmin):
   list_display = ['name', 'discounted_price', 'original_price', 'restaurant', 'image_url', 'valid_till', 'valid_from',
        'is_bumper', 'is_redeemable'
    ]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from',
                    'valid_till', 'discount',
                    'active', 'coupon_offer']
    list_filter = ['active', 'valid_from',
                   'valid_till']
    search_fields = ['code']
    exclude = ['code']
    #exclude = ['active']


class UserCouponAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'used_at',]
    search_fields = ['coupon__code']
    readonly_fields = ('used_at', )



admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ReviewLike, ReviewLikeAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(UserCoupon, UserCouponAdmin)
admin.site.register(Review)
admin.site.register(AdminAd)
admin.site.register(UserOffers)
admin.site.register(Tag)