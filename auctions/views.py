from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from auctions.forms import *

from .models import User, Listing


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def add_listing(request):

    if request.method == "POST":
        
        # Add current user to the model form
        listing=Listing(seller=request.user)
        
        # Get form data
        f = ListingForm(request.POST, instance=listing)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/add_listing.html",{
                "form": f
            })
        
    return render(request, "auctions/add_listing.html", {
        "form": ListingForm()
    })


def listing_page(request, listing_id):
    # Get user
    user = request.user

    # Get listing
    listing1 = Listing.objects.filter(pk=listing_id)
    listing = listing1.first()
    
    # Make a bid
    if request.POST.get("form_type") == "bid_form":
        
        # Get bid from post
        try: 
            bid = int(request.POST.get("new_bid"))
        except ValueError: 
            return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))

        # Show last bid. If there's no prior one, set first to 0.
        price = Bids.objects.filter(listing_id=listing_id)
        if price:
            price = Bids.objects.filter(listing_id=listing_id).last()
        else:
            price = Bids(amount='0', bidder=user, listing_id=listing)

        # Save if bid is larger or equal to min bid, and larger than prior bid.
        if bid >= listing.min_bid and bid > int(price.amount):
            bid = Bids(amount=bid, bidder=user, listing_id=listing)
            bid.save()
        else:
            return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))

        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
        
    
    # Add to a watchlist
    if request.POST.get("form_type") == "watchlist_form_add":
        w = Watchlist(user=user)
        w.save()
        w.listing_id.add(listing)

    # Remove from a watchlist
    if request.POST.get("form_type") == "watchlist_form_remove":
        w = Watchlist.objects.filter(listing_id=listing.id, user=user)
        w.delete()

    # Add a comment
    if request.POST.get("form_type") == "comment_form":
        comment = Comments(user=user, listing_id=listing)
        f = CommentsForm(request.POST, instance=comment)
        if f.is_valid():
            f.save()
        return HttpResponseRedirect(reverse('listing_page', args=(listing_id,)))
    
    # Check if listing is already in a watchlist
    w_listings = Listing.objects.filter(watchlist_listing__listing_id=listing_id, watchlist_listing__user=user)
    
    if listing in w_listings:
        watched_listing = True
    else:
        watched_listing = False
    
    price = Bids.objects.filter(listing_id=listing_id).last()

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comment_f": CommentsForm(),
        "watched_listing": watched_listing,
        "comments": Comments.objects.filter(listing_id=listing_id),
        "price": price
    })


@login_required
def watchlist(request):

    # Get user
    user = request.user

    # Get listings from the user's watchlist
    listings = Listing.objects.filter(watchlist_listing__user=user)
    
    # Render user's watched listings
    return render(request, "auctions/watchlist.html",{
        "listings": listings
    })


def categories(request):
    categories = Categories.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
    })


def category_listings(request, category):
    listings = Listing.objects.filter(category=category)
    category_name = Categories.objects.get(pk=category)
    return render(request, "auctions/category_listings.html", {
        "listings": listings,
        "category": category_name
    })
  