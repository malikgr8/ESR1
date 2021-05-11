from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import random

from project.feed.models.offer import Offer


class UserOffers(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,)

    offer = models.ForeignKey(
        Offer,
        on_delete=models.SET_NULL,
        null=True,)

    class Meta:
        verbose_name = 'UserOffer'
        verbose_name_plural = 'UserOffers'
        unique_together = [('user', 'offer')]

    def __str__(self):
        return self.user.username