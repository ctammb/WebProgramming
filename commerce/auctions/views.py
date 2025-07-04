from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from .models import User

# testing push to GitHub

def index(request):
    return render(request, "auctions/index.html")

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
        form = ListingForm()

        return render(request, "auctions/create.html", {
            "form": form})

def listing(request, listing_id):
    # Placeholder for listing view logic
    return render(request, "auctions/listing.html", {
        "listing_id": listing_id
    })

def watchlist(request):
    # Placeholder for watchlist view logic
    return render(request, "auctions/watchlist.html")

def categories(request):
    # Placeholder for categories view logic
    return render(request, "auctions/categories.html")

def category(request, category_name):
    # Placeholder for category view logic
    return render(request, "auctions/category.html", {
        "category_name": category_name
    })

def close_listing(request, listing_id):
    # Placeholder for closing a listing logic
    return render(request, "auctions/close_listing.html", {
        "listing_id": listing_id
    })

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
