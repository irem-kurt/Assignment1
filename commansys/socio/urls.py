from django.urls import path
from . import views

urlpatterns = [

    path('community-create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('created-communities/', views.CreatedCommunitiesView.as_view(), name='created_communities'),
    path('all-communities/', views.AllCommunitiesView.as_view(), name='all_communities'),
    path('join-community/<int:community_id>/', views.JoinCommunityView.as_view(), name='join_community'),
    
]