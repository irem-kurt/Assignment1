from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('community-create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('created-communities/', views.CreatedCommunitiesView.as_view(), name='created_communities'),
    path('all-communities/', views.AllCommunitiesView.as_view(), name='all_communities'),
    path('join-community/<int:community_id>/', views.JoinCommunityView.as_view(), name='join_community'),

    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('community/<int:community_id>/create_post/', views.create_post, name='create_post'),
    #path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    path('community/<int:community_id>/', views.community_detail, name='community_detail'),



]