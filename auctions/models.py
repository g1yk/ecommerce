from datetime import time
from os import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from django.utils import timezone



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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users", default=1)
    category = models.ManyToManyField(Category, default=None, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    listing_status = models.CharField(max_length=16, default="disabled")


    def __str__(self):
        return self.title



class Comment(models.Model):
    listing =  models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="commenters", on_delete=models.CASCADE, default=1)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.listing.title, self.user)