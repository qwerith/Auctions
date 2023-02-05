import pickle
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist, Image


def index(request):
    listings_final = []
    listings = list(Listing.objects.all())
    for i in listings:
        image = Image.objects.get(listing_id=i.id)
        listings_final.append({"main_info": i, "image": image})
    return render(request, "auctions/index.html", {
        "listings": listings_final
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

def create_listings(request):
    if request.method == "POST" and request.user.is_authenticated and None not in [request.POST["title"], request.POST["description"], request.POST["starting_bid"]]:
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        file = request.POST["file"]
        user = User.objects.get(username=request.user)
        listing = Listing(title=title, description=description, starting_bid=starting_bid, owner=user)
        listing.save()
        file = Image(listing_id=listing, picture=file)
        file.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html")

def listing(request, owner, id):
    if request.method == "POST" and request.user.is_authenticated and None not in [request.POST["comment"], request.POST["description"], request.POST["starting_bid"]]:
        return HttpResponseRedirect(reverse("listing"))
    else:
        listings_final = []
        listing = Listing.objects.get(id=int(id))
        print(listing)
        image = Image.objects.get(listing_id=listing.id)
        listings_final.append({"main_info": listing, "image": image.picture})
        return render(request, "auctions/index.html", {
            "listings": listings_final
            })


#listing = Listing.objects.values('id')
        #print(listing)
        #bid = Bid(object_id=listing[0]["id"], user_id=user, amount=int(starting_bid))
        #bid.save()