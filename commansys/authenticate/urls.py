from django.urls import path


from . import views
from .views import RegisterView 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('profile/edit/<int:id>/', views.edit_profile, name='edit_profile'),

    path('profile/<int:id>/', views.view_profile, name='user-profile'),

    path('register/', RegisterView.as_view(), name='registerpage'),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
