""" Product Models """
import datetime
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField


class Category(models.Model):
    """ Model to assign a category to a product """

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Product(models.Model):
    """ Model to shape the product """

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    country = CountryField(max_length=254, null=True, blank=True)
    description = models.TextField()
    vintage = models.PositiveIntegerField(validators=[max_value_current_year])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.FloatField(default=0)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Model to allow reviewing of products """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
