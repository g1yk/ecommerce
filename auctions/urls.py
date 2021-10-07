from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.add_listing, name="new"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>", views.add_comment, name="add_comment"),
    path("close_listing/<int:listing_id>", views.close_listing, name="close_listing")


]
