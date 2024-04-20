from django.urls import path
from . import views

urlpatterns = [

    path('community/', views.CommunityCreateView.as_view(), name='community-create'),
    path('community/<int:pk>', views.CommunityView.as_view(), name='community'),
    #path('community/add', views.CommunityCreateView.as_view(), name='community/add')

]