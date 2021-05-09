from django.db import models

from project.feed.models.review import Review


def review_image_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/users/{instance.review.user.id}/reviews/review'


class ReviewImage(models.Model):

    image_url = models.ImageField(upload_to=review_image_path)
    review = models.ForeignKey(Review, verbose_name="reveiew_id", on_delete=models.CASCADE)

    def __str__(self):
        return self.image_url.url
