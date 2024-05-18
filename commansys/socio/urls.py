from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"), # This is the home page
    path('community-create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('created-communities/', views.CreatedCommunitiesView.as_view(), name='created_communities'),
    path('all-communities/', views.AllCommunitiesView.as_view(), name='all_communities'),
    path('join-community/<int:community_id>/', views.JoinCommunityView.as_view(), name='join_community'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', views.dislike_post, name='dislike_post'),
    path('post/like_dislike/', views.like_dislike_post, name='like_dislike_post'),
    path('post/add_comment/', views.add_comment, name='add_comment'),
    path('community/<int:community_id>/create_post/', views.create_post, name='create_post'),
    path('community/<int:community_id>/create_custom_post/<int:template_id>', views.create_custom_post, name='create_custom_post'),
    path('community/<int:community_id>/create_template/', views.create_template, name='create_template'),
    path('community/quit/', views.community_quit, name='community_quit'),
    path('community/join/', views.community_join, name='community_join'),
    path('community/request/', views.community_request, name='community_request'),
    path('community/response/', views.community_response, name='community_response'),
    path('community/make_remove_manager/', views.make_remove_manager, name='make_remove_manager'),
    path('community/<int:community_id>/requests/', views.display_requests, name='display_requests'),
    path('community/<int:community_id>/followers/', views.display_followers, name='display_followers'),
    path('community/<int:community_id>/advanced_search', views.advanced_search, name='community-advanced-search'),
    path('community/<int:community_id>/', views.community_detail, name='community_detail'),
    path('user/follow_unfollow/', views.follow_unfollow, name="follow_unfollow"),
]