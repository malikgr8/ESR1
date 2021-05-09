import datetime

from django.db import models


def image_upload_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/admin_ads/{datetime.datetime.utcnow()}/title/'


class AdminAd(models.Model):

    SILVER = 'S'
    GOLD = 'G'
    DIAMOND = 'D'

    CATEGORY_CHOICES = [
        (SILVER, 'Silver'),
        (GOLD, 'Gold'),
        (DIAMOND, 'Diamond'),
    ]

    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=SILVER)
    expiry = models.DateTimeField(auto_now=False, auto_now_add=False)
    deeplink = models.URLField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
