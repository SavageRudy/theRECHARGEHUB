from django.urls import path
from . import views


urlpatterns = [
      path("", views.index),
      path("login" , views.login_request),
      path("register", views.register),
      path("logout", views.logout_request),
      path("browse", views.browse),
      path("profile", views.profile),
      path("combo", views.combo),
      path("internet", views.internet),
      path("talk", views.talk),
      path("checkout", views.checkout),
     

  ]