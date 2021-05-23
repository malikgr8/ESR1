import datetime

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django_countries.fields import CountryField

from project.feed.models import Category


def image_upload_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/restaurants/{instance.name}/restaurant_image/{datetime.datetime.utcnow()}'


def logo_upload_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/restaurants/{instance.name}/restaurant_logo/{datetime.datetime.utcnow()}'


def cover_upload_path(instance, filename):
    """
    This function returns path of image to be stored
    """

    return f'images/restaurants/{instance.name}/restaurant_cover/{datetime.datetime.utcnow()}'


class Restaurant(models.Model):

    name = models.CharField(verbose_name='restaurant_name', max_length=50)
    website = models.URLField(verbose_name='restaurant_website', blank=True)

    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: "
                "'+999999999'. Up to 15 digits allowed."
    )

    phone_number = models.CharField(verbose_name='restaurant_phone_number', validators=[phone_regex], max_length=15)
    email = models.EmailField(verbose_name='restaurant_email', blank=True)
    opening_hours = models.CharField(verbose_name='restaurant_opening_hours', max_length=50)

    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    PRICE_LEVEL_CHOICES = (
        (LOW, '$'),
        (MEDIUM, '$$'),
        (HIGH, '$$$'),
    )

    DINE_IN = 'DINE IN ONLY'
    DINE_IN_TAKE_AWAY = 'DINE IN & TAKE AWAY'
    DINE_IN_DELIVERY = 'DINE IN & DELIVERY'
    TAKE_AWAY = 'TAKE AWAY ONLY'
    TAKE_AWAY_DELIVERY = 'TAKE AWAY & DELIVERY'
    DELIVERY = 'DELIVERY ONLY'
    DINE_IN_TAKE_AWAY_DELIVERY = 'DINE IN & TAKE AWAY & DELIVERY'

    RESTAURANT_TYPE_CHOICES = (
        (DINE_IN, 'Dine In Only'),
        (DINE_IN_TAKE_AWAY, 'Dine In & Take Away'),
        (DINE_IN_DELIVERY, 'Dine In & Delivery'),
        (TAKE_AWAY, 'Take Away Only'),
        (TAKE_AWAY_DELIVERY, 'Take Away & Delivery'),
        (DELIVERY, 'Delivery Only'),
        (DINE_IN_TAKE_AWAY_DELIVERY, 'Dine In & Take Away & Delivery'),
    )

    price_level = models.CharField(verbose_name='restaurant_price_level', max_length=6, choices=PRICE_LEVEL_CHOICES)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='restaurants',
        null=True,
        blank=True,
    )
    restaurant_type = models.CharField(
        max_length=50, 
        choices=RESTAURANT_TYPE_CHOICES, 
        default=DINE_IN_TAKE_AWAY_DELIVERY
    )

    country = CountryField(blank_label='(select country)')
    city = models.CharField(verbose_name='restaurant_city', max_length=50)
    address = models.CharField(verbose_name='restaurant_address', max_length=256, blank=True, null=True)
    zip_code = models.CharField(verbose_name='restaurant_zip_code', max_length=10, blank=True, null=True)
    lat = models.FloatField(verbose_name='latitude', blank=True, null=True)
    long = models.FloatField(verbose_name='logitude', blank=True, null=True)

    created = models.DateTimeField(verbose_name='date_created', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='date_modified', auto_now=True)

    image = models.ImageField(upload_to=image_upload_path, verbose_name='restaurant_image', blank=True)
    logo_image = models.ImageField(upload_to=logo_upload_path, verbose_name='restaurant_logo_image', blank=True)
    cover_image = models.ImageField(upload_to=cover_upload_path, verbose_name='restaurant_cover_image', blank=True)
    
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return self.name
