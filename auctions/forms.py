from django import forms
from django.contrib.auth import models
from django.db.models import fields


from .models import Category, Comment, ListingStatus, User, Listing, Bid





class ListingForm(forms.ModelForm):
    category = forms.CharField()
    

    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "photo",
            "category",
            "end_date"
        ]
    

    def save(self, commit=True):
        category, created = Category.objects.get_or_create(
            name = self.cleaned_data['category']
        )
        self.cleaned_data['category'] = category.id
        return super(ListingForm, self).save(commit)

    def __str__(self):
        return self.title

# class ListingForm(forms.Form):
#     id = forms.IntegerField(required=False, widget=forms.HiddenInput())
#     listing = forms.ModelChoiceField(queryset=Listing.objects.all())
#     category = forms.ModelChoiceField(queryset=Category.objects.all())


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ('user',)
        fields = [
            "amount"
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'body'
        ]

# class ListingStatusForm(forms.ModelForm):
#     class Meta:
#         model = ListingStatus
#         fields = [

#         ]
