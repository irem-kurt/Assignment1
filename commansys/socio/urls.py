from django.urls import path
from . import views

urlpatterns = [

    path('community-create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('community/', views.PublicCommunityView.as_view(), name='community-view'),
    #path('community/add', views.CommunityCreateView.as_view(), name='community/add')

]