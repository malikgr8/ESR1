import datetime
from decimal import Decimal

from django.db import models
from .restaurant import Restaurant


def offer_image_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/restaurants/{instance.restaurant.name}/offers/{datetime.datetime.utcnow()}'


class Offer(models.Model):

    name = models.CharField(verbose_name='offer_name', max_length=256)
    discounted_price = models.FloatField(blank=True, null=True, default=0.0)
    original_price = models.FloatField(default=0.0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True)

    image_url = models.ImageField(upload_to=offer_image_path)
    valid_from = models.DateTimeField()
    valid_till = models.DateTimeField()
    approval_status = models.BooleanField(default=False)
    is_bumper = models.BooleanField(default=False)
    is_redeemable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
