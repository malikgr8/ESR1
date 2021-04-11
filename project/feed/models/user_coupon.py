from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random

from project.feed.models.coupon import Coupon


class UserCoupon(models.Model):

    REDEEM_LIMIT = 5

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,)

    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)
