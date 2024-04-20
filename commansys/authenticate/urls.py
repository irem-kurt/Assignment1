from django.urls import path


from . import views
from .views import RegisterView  # Import the view here

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name='home'),

    path('profile/<int:id>/', views.user_profile, name='user-profile'),

    path('register/', RegisterView.as_view(), name='register'),


    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
]
