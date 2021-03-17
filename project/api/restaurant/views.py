#from urllib import request
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from project.api.base import GetObjectMixin
from project.api.categories.serializers import CategorySerializer
from project.api.permissions import IsUserOrReadOnly
from project.api.restaurant.serializers import RestaurantSerializer, RestaurantImageUploadSerializer, OfferSerializer
from project.feed.models import Restaurant, Category, Offer
from project.feed.models.coupon import Coupon
from project.feed.models.forms import CouponApplyForm
from project.feed.models.offer import Offer
import time as _time

#from urllib3.util import request


class ListAllRestaurantsView(ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def filter_queryset(self, queryset):
        search_string = self.request.query_params.get('search')
        if search_string:
            queryset = queryset.filter(Q(name__icontains=search_string) |
                                       Q(country__icontains=search_string) |
                                       Q(street__icontains=search_string) |
                                       Q(city__icontains=search_string)).order_by('reviews')
        return queryset


class NewRestaurantView(GenericAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        restaurant = serializer.create(serializer.validated_data)
        return Response(RestaurantSerializer(restaurant).data, status.HTTP_201_CREATED)


class RestaurantImageUploadView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, **kwargs):
        serializer = RestaurantImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Ok')


class RestaurantGetUpdateDeleteView(GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [
        IsUserOrReadOnly,
    ]

    def get(self, request, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, **kwargs):
        restaurant = self.get_object()
        serializer = self.get_serializer(restaurant, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        restaurant = self.get_object()
        restaurant.delete()
        return Response('Deleted', status.HTTP_200_OK)


class ListCategoryRestaurantsView(GetObjectMixin, ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

    def filter_queryset(self, queryset):
        category = self.get_object_by_model(Category, pk=self.kwargs.get('pk'))
        return queryset.filter(category=category)


class UserRestaurantsView(ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(user__username=self.request.user.username).order_by('created')


class AllOffers(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        return Offer.objects.filter(approval_status=True)


class OfferByName(GenericAPIView):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()

    def get(self, request, **kwargs):
        import pdb;pdb.set_trace()
        offer = self.queryset.filter(name=request.data.get('offer_name'), approval_status=True)
        serializer = self.get_serializer(offer, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class OfferByRestaurant(GenericAPIView):
    #id = Offer.objects.get(OfferSerializer)
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #queryset = Offer.objects.all()

    def get(self, request, **kwargs):
        offer = self.queryset.filter(restaurant_id=kwargs.get('restaurant_id'), approval_status=True)
        serializer = self.get_serializer(offer, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, **kwargs):
        """
        create offer
        :param request:
        :param kwargs:
        :return:
        """

        offer_serializer = self.get_serializer(data=request.data, context={'request': request})
        offer_serializer.is_valid(raise_exception=True)
        offer_serializer.save()
        return Response(offer_serializer.data, status.HTTP_201_CREATED)


@require_POST
def coupon_apply(request):
    now = _time.timezone.now()
    form = CouponApplyForm(request.Post)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon-id'] = None
        return redirect('offer:offer_detail')