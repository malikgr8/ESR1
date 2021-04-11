from django.db import models

from project.feed.models.restaurant import Restaurant


class MenuImage(models.Model):

    image = models.ImageField()
    sort_order = models.SmallIntegerField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.url