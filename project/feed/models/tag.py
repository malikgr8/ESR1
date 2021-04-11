from django.db import models
from project.feed.models.restaurant import Restaurant

from project.feed.models.coupon import Coupon


class Tag(models.Model):

    name = models.CharField(max_length=50)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name