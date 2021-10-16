from datetime import time
from os import name
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from django.utils import timezone



class User(AbstractUser):
    pass




class Category(models.Model):
    name = models.CharField(max_length=64)

    # class Meta:
    #  ordering = ('name',)
    #  verbose_name = 'category'
    #  verbose_name_plural = 'categories'
    #
    # test
    def __str__(self):
        return self.name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    photo = models.CharField(max_length=1024, null=True)
    # bid = models.ForeignKey(
    #     Bid, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="users", default=1
    )
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyers", blank=True, default=1
    )
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sellers", blank=True, default=1
    )
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidders", blank=True, default=1
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=24, decimal_places=2)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_price", default=None)


    def __str__(self):
        return f"{self.item} ({self.amount}) by {self.user}"


# class Image(models.Model):
#     photo = models.ImageField(null=True)
#     image_url = models.CharField(max_length=1024, null=True)
#     item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_photo")



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item_watchlist")

    def __str__(self):
        return 'User={0}, Listing={1}'.format(self.user, self.item)



class ListingStatus(models.Model):
    ENABLED = "Enabled"
    DISABLED = "Disabled"
    STATUS_CHOICES = [(ENABLED, "Enabled"), (DISABLED, "Disabled")]
    listing = models.ForeignKey(
        Listing, related_name="statuses", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=DISABLED)


    def __str__(self):
       return self.status

class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, related_name="comments", on_delete=models.CASCADE, default=None
    )
    user = models.ForeignKey(
        User, related_name="commenters", on_delete=models.CASCADE, default=1
    )
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.listing.title, self.user)
