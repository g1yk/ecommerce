from auctions.forms import BidForm, CommentForm, ListingForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, Comment, ListingStatus, User, Listing


def index(request):
    
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all()
    })



def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing_status = ListingStatus.objects.get(listing=listing)
    message = ""
    comments = listing.comments.filter()
    new_comment = None

    if request.method == "POST":
        
        if request.POST.get('amount'):
            form = BidForm(request.POST)
            if form.is_valid():
                bid = form.cleaned_data['amount']
                print(form.cleaned_data)
                if listing.price >= bid:
                    message = "Your bid is lower than the last bid"
                else:
                    listing.price = bid
                    listing.user = request.user
                    listing.save()

                    print('USER: ', listing.user, request.user)
                return render(request, 'auctions/listing.html', {
                    "listing":listing,
                    "bid":bid,
                    "message":message
                })
        if request.POST.get('body'):
           
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.listing = listing
                new_comment.user = request.user
                new_comment.save()
            else:
                comment_form = CommentForm()

    return render(request, 'auctions/listing.html', {
        'listing_status':listing_status,
        "listing":listing,
        'comments':comments,
        'new_comment':new_comment
    })

def add_comment(request):
    if request.method == "POST":
        print("YAY")
        pass
  

def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user = request.user
            new_listing.listing_status = "enabled"
            new_listing.save()

            listing_status = ListingStatus(listing=new_listing, status = "Enabled")
            listing_status.save()
            print('LISTING STATUS ', listing_status.pk)

            # listing_status = ListingStatus.objects.get(pk=new_listing.pk)
            # listing_status.status = 'Enabled'
            # listing_status.save()

            return HttpResponseRedirect(reverse('listing', args=(new_listing.pk,)))
        else:
            return render(request, "auctions/new.html",{
                'category':Category.objects.all()
            })
    else:
        return render(request, "auctions/new.html",{
            'category':Category.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
