from django.db import models

from project.feed.models.coupon import Coupon


class Tag(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name