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
from rest_framework import mixins
from datetime import datetime

User = get_user_model()


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

    def post(self, request):
        """
        use coupon by promo code given by restaurant
        """
        user = request.user
        coupon_code = request.data.get('coupon_code')
        coupon = Coupon.objects.get(code=coupon_code)
        if coupon:
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
        else:
            return Response(
                {
                    'message': "Invalid coupon code.",
                    'coupon_applied': False
                }
            )