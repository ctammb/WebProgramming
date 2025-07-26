from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.active_listings, name="index"),
    path("index", views.active_listings, name="active_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("closed/", views.closed_listings, name="closed_listings"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:name>", views.category, name="category"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist/toggle/<int:listing_id>/", views.toggle_watchlist, name="toggle_watchlist")
    ]

