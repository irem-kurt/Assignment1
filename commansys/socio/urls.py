from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"), # This is the home page (index)
    path('community-create/', views.CommunityCreateView.as_view(), name='community-create'),
    path('all-communities/', views.AllCommunitiesView.as_view(), name='all_communities'), # My Communities Tab

    path('community/<int:community_id>/create_post/', views.create_post, name='create_post'), # Default post creation page
    path('community/<int:community_id>/create_custom_post/<int:template_id>', views.create_custom_post, name='create_custom_post'), # Custom post creation page
    path('community/<int:community_id>/create_template/', views.create_template, name='create_template'), # Custome post template creation page
    
    # Community detail page
    path('community/<int:community_id>/', views.community_detail, name='community_detail'),
    path('post/like_dislike/', views.like_dislike_post, name='like_dislike_post'), # AJAX call for like and dislike
    path('post/add_comment/', views.add_comment, name='add_comment'), # AJAX call for adding comment
    path('community/quit/', views.community_quit, name='community_quit'), # AJAX call for quitting community
    path('community/join/', views.community_join, name='community_join'), # AJAX call for joining community
    path('community/request/', views.community_request, name='community_request'), # AJAX call for requesting to join community
    
    # Community Requests page
    path('community/<int:community_id>/requests/', views.display_requests, name='display_requests'),
    path('community/response/', views.community_response, name='community_response'), # AJAX call for responding to join request
    
    # Community Followers page
    path('community/<int:community_id>/followers/', views.display_followers, name='display_followers'),
    path('community/make_remove_manager/', views.make_remove_manager, name='make_remove_manager'), # AJAX call for making or removing manager
    
    # Community Advanced Search page
    path('community/<int:community_id>/advanced_search', views.advanced_search, name='community-advanced-search'),
    
    path('user/follow_unfollow/', views.follow_unfollow, name="follow_unfollow"), # AJAX call for follow and unfollow users, doesnt work in authenticate app so moved here
]