from django import forms
from django.contrib.auth import models
from django.db.models import fields


from .models import Category, Comment, User, Listing, Bid



class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

class ListingForm(forms.ModelForm):
    category = forms.CharField()
    

    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "price",
            "photo",
            "category"
        ]
        widgets = {
            "end_date": DateForm()
        }

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

