from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ListingForm, BidForm
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Category, Watchlist
from django.contrib import messages


def active_listings(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "view_title": "Active Listings"
        })

def closed_listings(request):
    listings = Listing.objects.filter(is_active=False)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "view_title": "Closed Listings"
    })

@login_required
def create(request):
    if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to create a listing.")
    
    if request.method == "POST":

        # Extract form data

        form = ListingForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            listing = form.save(commit=False)
            print(f"User: {request.user} (Authenticated: {request.user.is_authenticated})")
            listing.owner = request.user  # Set the owner to the current user
            print(f"Listing owner set to: {listing.owner.username}")
            try:
                listing.save()
                print("Listing saved successfully")
            except Exception as e:
                print(f"Error saving listing: {e}")
            return HttpResponseRedirect(reverse("index"))
        else:
            print("Form is invalid")
            form = ListingForm()
            return render(request, "auctions/create.html", {
            "form": form})

    else:
        form = ListingForm()
        return render(request, "auctions/create.html", {
            "form": form})

@login_required
def listing(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to view listing and place a bid.")
    
    highest_bid = listing.highest_bid
    min_bid = highest_bid.amount if highest_bid else listing.starting_bid

    if request.method == "POST":

        form = BidForm(request.POST, min_bid=min_bid)
        if form.is_valid():
            print("Form is valid")
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = listing

            if bid.amount <= min_bid:
                form.add_error('amount', f'Bid must be greater than the current price (${min_bid})')
            else:
                bid.save()
                print("Bid saved successfully")
                return redirect('listing', listing_id=listing.id)

    else:
        form = BidForm(min_bid=min_bid)
    
    highest_bid = listing.highest_bid
    user_is_highest_bidder = (
        request.user.is_authenticated and
        highest_bid and
        highest_bid.bidder == request.user
    )

    is_watching = False
    if request.user.is_authenticated:
        is_watching = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    is_owner = False
    if request.user == listing.owner:
        is_owner = True

    winning_bid = listing.bids.order_by('-amount').first()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "user_is_highest_bidder": user_is_highest_bidder,
        "is_watching": is_watching,
        "is_owner": is_owner,
        "winning_bid": winning_bid
    })

@login_required
def listing(request, listing_id):

    listing = get_object_or_404(Listing, pk=listing_id)

    if not request.user.is_authenticated:
            return HttpResponse("You must be logged in to view listing and place a bid.")
    
    highest_bid = listing.highest_bid
    min_bid = highest_bid.amount if highest_bid else listing.starting_bid

    if request.method == "POST":

        form = BidForm(request.POST, min_bid=min_bid)
        if form.is_valid():
            print("Form is valid")
            bid = form.save(commit=False)
            bid.bidder = request.user
            bid.listing = listing

            if bid.amount <= min_bid:
                form.add_error('amount', f'Bid must be greater than the current price (${min_bid})')
            else:
                bid.save()
                print("Bid saved successfully")
                return redirect('listing', listing_id=listing.id)

    else:
        form = BidForm(min_bid=min_bid)
    
    highest_bid = listing.highest_bid
    user_is_highest_bidder = (
        request.user.is_authenticated and
        highest_bid and
        highest_bid.bidder == request.user
    )

    is_watching = False
    if request.user.is_authenticated:
        is_watching = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    is_owner = False
    if request.user == listing.owner:
        is_owner = True

    winning_bid = listing.bids.order_by('-amount').first()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "user_is_highest_bidder": user_is_highest_bidder,
        "is_watching": is_watching,
        "is_owner": is_owner,
        "winning_bid": winning_bid
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    watch_entry, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)

    if not created:
        watch_entry.delete()
    else:
        messages.success(request, "Added to your watchlist.")

    return redirect("listing", listing_id=listing.id)

@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlist__user=request.user)
    return render(request, "auctions/watchlist.html", {"listings": listings})


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories":categories})

def category(request, name):
    category = get_object_or_404(Category, name=name)
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })


def close_listing(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        if request.user == listing.owner:
            listing.is_active = False
            listing.save()

            # Get the winning bid
            winning_bid = listing.bids.order_by('-amount').first()

            # Optional: pass context if redirecting
            return redirect('listing', listing_id=listing.id)

    return redirect('index')


def add_bid(request, listing_id):
    # Placeholder for adding a bid logic
    return render(request, "auctions/add_bid.html", {
        "listing_id": listing_id
    })

def add_comment(request, listing_id):
    # Placeholder for adding a comment logic
    return render(request, "auctions/add_comment.html", {
        "listing_id": listing_id
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
