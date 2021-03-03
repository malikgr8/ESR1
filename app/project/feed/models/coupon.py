from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from project.feed.models.offer import Offer
import random


class Coupon(models.Model):
    code=models.CharField(max_length=50, unique=True)
    valid_from=models.DateTimeField()
    valid_till = models.DateTimeField()
    discount =models.IntegerField(validators=[MinValueValidator(0),
                                              MaxValueValidator(100)])
    active = models.BooleanField()

    coupon_offer = models.ForeignKey(
        Offer,
        on_delete=models.SET_NULL,
        related_name='offers',
        null=True,)

    def save(self, *args, **kwargs):
        if self._state.adding:

            while(1):
                code1 = str(random.randint(1000, 9999))
                if not Coupon.objects.filter(code=code1).exists():
                    break

            self.code=code1
            pass

        super(Coupon, self).save(*args, **kwargs)

    def __str__(self):
        return self.code
