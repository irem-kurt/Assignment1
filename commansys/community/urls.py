from django.urls import path
from django.contrib import admin
from django.urls import path
from .models import Community, UserProfile
from . import views
from .views import Index, ProfileView


urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("community/", views.community, name="community"),
    path("user/", views.user, name="user"),
    #path("create", views.create, name="create"),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),

]

