from auctions.forms import BidForm, ListingForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Category, User, Listing


def index(request):
    category = None
    categories = Category.objects.all()

    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all(),
        "category":Category.objects.all()
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    message = ""

    if request.method == "POST":
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
            return render(request, 'auctions/listing.html', {
                "listing":listing,
                "bid":bid,
                "message":message
            })

    return render(request, 'auctions/listing.html', {
        "listing":listing
    })

# def bid_update(request):
  


def add_listing(request):
    
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            new_listing = form.save()
            return HttpResponseRedirect(reverse(listing, args={new_listing.pk,}))
    else:
        return render(request, "auctions/new.html",{
            "category":Category.objects.all()
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
