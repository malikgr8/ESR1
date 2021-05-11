from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.api.me.serializers import UserSerializer, UserProfileUpdateSerializer
from project.api.permissions import IsUserOrReadOnly
from rest_framework.decorators import api_view
from django.contrib import auth
from django.contrib.auth.models import User

from project.feed.models.coupon import Coupon
from project.feed.models.user_coupon import UserCoupon
from project.feed.models.user_offers import UserOffers
from rest_framework import mixins
from datetime import datetime
from datetime import timedelta
from rest_framework.views import APIView
from project.api.restaurant.serializers import OfferSerializer
from project.api.me.serializers import UserCoupnSerializer, UserOfferSerializer
from project.feed.models.offer import Offer
import pytz


User = get_user_model()


class GetUserProfileView(GenericAPIView):

    permission_classes = [
        IsAuthenticated,
        IsUserOrReadOnly
    ]

    def get(self, request, **kwargs):
        user = User.objects.get(pk=request.user.id)
        return Response(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone_number": user.username
            }
        )

class GetUpdateUserProfileView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
        IsUserOrReadOnly
    ]

    def get(self, request, **kwargs):
        return Response(self.get_serializer(request.user).data)

    def post(self, request, **kwargs):
        serializer = UserProfileUpdateSerializer(data=request.data, context={
            'request': request
        })
        serializer.is_valid(raise_exception=True)
        user = serializer.save(serializer.validated_data)
        return Response(self.get_serializer(user).data)

    def delete(self, request, **kwargs):
        user = self.request.user
        user.is_active = False
        user.save()
        return Response('OK')


#####################################################
class CouponApply(mixins.CreateModelMixin, GenericAPIView):
    permission_classes = [
            IsAuthenticated,
            IsUserOrReadOnly
    ]
    
    def post(self, request):
        """
        use coupon by promo code given by restaurant
        """
        user = request.user
        coupon_code = request.data.get('coupon_code')
        offer_id = request.data.get('offer_id')
        try:
            offer = Offer.objects.get(pk=offer_id)
            try:
                coupon = Coupon.objects.get(code=coupon_code, coupon_offer=offer)
                already_used_coupon = UserCoupon.objects.filter(user=user, coupon=coupon).order_by('-used_at')
                if already_used_coupon:
                    re_usable_time = already_used_coupon[0].used_at + timedelta(hours=UserCoupon.REDEEM_HOURS_LIMIT)
                    if re_usable_time > datetime.now().replace(tzinfo=pytz.UTC):
                        return Response(
                            {
                                'message': "Coupon can not be redeemable before 24 hours.",
                                'coupon_applied': False
                            }
                        )
                user_coupon = UserCoupon(
                    user=user,
                    coupon=coupon,
                    used_at=datetime.now()
                )
                user_coupon.save()
                return Response(
                    {
                        'message': "Coupon successfully applied.",
                        'coupon_applied': True
                    }
                )
            except Coupon.DoesNotExist:
                return Response(
                {
                    'message': "Invalid Coupon code.",
                    'coupon_applied': False
                }
            )
        except Offer.DoesNotExist:
            return Response(
                {
                    'message': "Invalid offer.",
                    'coupon_applied': False
                }
            )



class UserCouponsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        offers = []
        info = UserCoupon.objects.filter(user=request.user)
        info = UserCoupnSerializer(info, context={'request': request}, many=True).data
        return Response(info)


class UserFavOffersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        info = UserOffers.objects.filter(user=request.user).select_related('offer')
        info = UserOfferSerializer(info, context={'request': request}).data
        return Response(info)


class GetUserOfferView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, **kwargs):
        info = UserOffers.objects.filter(user=request.user, offer=kwargs.get('offer_id')).select_related('offer')
        info = UserOfferSerializer(info).data
        return Response(info)


class AddUserFavOfferView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        try:
            offer = Offer.objects.get(pk=request.data.get('offer_id'))
            fav_offer = UserOffers(
                user=user,
                offer=offer
            )
            fav_offer.save()
            return Response({
                'message': 'offer added into favourites.',
                'code': 200
            })
        except:
            return Response({
                'message': 'Invalid offer id.',
                'code': 422
            })

class RemoveUserFavOfferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            UserOffers.objects.get(user=request.user, offer=request.data.get('offer_id')).delete()
            return Response({
                'message': 'offer deleted from favourites.',
                'code': 200
            })
        except:
            return Response({
                'message': 'Invalid offer id.',
                'code': 422
            })
