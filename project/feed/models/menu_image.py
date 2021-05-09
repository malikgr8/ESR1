import datetime

from django.db import models

from project.feed.models.restaurant import Restaurant


def image_upload_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/restaurants/{instance.restaurant.name}/menu/{datetime.datetime.utcnow()}'


class MenuImage(models.Model):

    image = models.ImageField(upload_to=image_upload_path)
    sort_order = models.SmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url
