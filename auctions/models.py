from os import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.urls import reverse


class User(AbstractUser):
    pass



class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=24, decimal_places=2)

    def __str__(self):
        return f"{self.current_price} ({self.newBid})"

class Category(models.Model):
    name = models.CharField(max_length=64)

    # class Meta:
    #  ordering = ('name',)
    #  verbose_name = 'category'
    #  verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    photo = models.ImageField()
    # image_url = models.URLField(blank=true)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ManyToManyField(Category, default=None)

    def __str__(self):
        return self.title