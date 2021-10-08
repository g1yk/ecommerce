from auctions.forms import BidForm, CommentForm, ListingForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date
from django.utils import timezone
from datetime import datetime



from .models import Category, Comment, ListingStatus, User, Listing


def index(request):
    
    return render(request, "auctions/index.html",{
        "listings":Listing.objects.all(),
        "statuses":ListingStatus.objects.filter(status="Enabled")
    })

def is_past_due(self):
    return date.today() > self.date

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing_status = ListingStatus.objects.get(listing=listing)
    message = ""
    comments = listing.comments.filter()
    new_comment = None

    print('IS PAST?? ', 'Ending date ', listing.end_date, 'Now ', timezone.now())
    print(listing.end_date.hour, timezone.now().hour)
    days_left = listing.end_date.day - datetime.now().day
    hours_left = listing.end_date.hour - timezone.now().hour
    minutes_left = listing.end_date.minute - timezone.now().minute
    seconds_left = listing.end_date.second - timezone.now().second


    print(f'{days_left} Days left, {hours_left} hours and {minutes_left} minutes and {seconds_left} seconds.')

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
                    listing.bidder = request.user
                    listing.save()

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
            new_listing.seller = request.user
            new_listing.listing_status = "enabled"
            #  Applying time
            new_listing.end_date = new_listing.end_date.replace(hour=new_listing.created_at.hour, minute=new_listing.created_at.minute, second=new_listing.created_at.second)

            new_listing.save()

            listing_status = ListingStatus(listing=new_listing, status = "Enabled")
            listing_status.save()


            return HttpResponseRedirect(reverse('listing', args=(new_listing.pk,)))
        else:
            return render(request, "auctions/new.html",{
                'category':Category.objects.all()
            })
    else:
        return render(request, "auctions/new.html",{
            'category':Category.objects.all()
        })

def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing_status = ListingStatus.objects.get(listing=listing)

    if request.method == "POST":
        print('hello')
        listing_status.status = "Disabled"
        print(listing_status)
        listing_status.save()
        listing.buyer = listing.bidder
        listing.save()
    
    return render(request, 'auctions/listing.html', {
            "listing":listing,
            "listing_status":listing_status
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
