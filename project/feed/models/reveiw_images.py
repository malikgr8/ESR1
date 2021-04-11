from django.db import models

from project.feed.models.review import Review


class ReviewImage(models.Model):

    image_url = models.ImageField()
    review = models.ForeignKey(Review, verbose_name="reveiew_id", on_delete=models.CASCADE)

    def __str__(self):
        return self.image_url.url