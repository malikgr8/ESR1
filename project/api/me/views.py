from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from project.api.me.serializers import UserSerializer, UserProfileUpdateSerializer
from project.api.permissions import IsUserOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import auth
from django.contrib.auth.models import User

from project.feed.models.coupon import Coupon
from project.feed.models.user_coupon import UserCoupon

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

@api_view(['POST'])
def use_Coupon(request):
    data = {
        'status': 0
    }
    try:
        code = request.data['code']
        user_id = request.data['user_id']

        if Coupon.objects.filter(code=code, active=True).exists():
            coupon = Coupon.objects.get(code=code)
            user = User.objects.get(id=user_id)
            UserCoupon.objects.create(user=user, coupon=coupon)
            data['status'] = 1
            pass

    except Exception as e:
        print(e)
        pass

    return Response(data=data)

