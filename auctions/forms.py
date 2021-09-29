from django import forms
from django.contrib.auth import models
from django.db.models import fields


from .models import User, Listing, Bid


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "category",
            "description",
            "price",
            "photo"
        ]

    def __str__(self):
        return self.title


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('user',)
        fields = [
            "amount"
        ]
