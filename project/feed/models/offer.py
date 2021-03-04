from datetime import datetime
from decimal import Decimal

from django.conf import settings
#import self as self
from django.db import models
from .restaurant import Restaurant
#from project.feed.models.coupon import Coupon


class Offer(models.Model):

    name = models.CharField(
        verbose_name='offer_name',
        max_length=256
    )
    discounted_price = models.FloatField(
        blank=True,
        null=True,
        default=0.0
    )
    orignal_price = models.FloatField(
        default=0.0
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        related_name='offers',
        null=True,
    )

    #coupon=models.ForeignKey(Coupon,
     #                        related_name='coupon',
      #                       null=True, blank=True,
       #                      on_delete=models.CASCADE)

    #def __init__(self):
     #   self.coupon_id = self.session.get('coupon_id')


    image_url = models.ImageField()
    valid_from = models.DateTimeField()
    valid_till = models.DateTimeField()
    approval_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=datetime.now())
    updated_at = models.DateTimeField(default=datetime.now())

    def __str__ (self):
        return self.name
