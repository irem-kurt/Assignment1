from datetime import timezone
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.contrib import messages



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Community, Post
from .forms import CommentForm, CommunityForm, PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Community, NotifyUser
from .forms import CommunityForm

from django.shortcuts import redirect

class CommunityCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CommunityForm()
        context = {
            'form': form,
        }
        return render(request, 'socio/communitycreate.html', context)
        
    
    def post(self, request, *args, **kwargs):
        communities = Community.objects.all().order_by('-createdDate')
        form = CommunityForm(request.POST, request.FILES)
        if form.is_valid():
            new_community = form.save(commit=False)
            new_community.location = form.save

            new_community.owner = request.user
            
            new_community.save()
            messages.success(request, 'Community creation is successful.')
        context = {
            'community_list': communities,
            'form': form,
        }
        return render(request, 'socio/communitycreate.html', context)


class CreatedCommunitiesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.filter(owner=request.user).order_by('-createdDate')
        form = CommunityForm()  
        number_of_created_communities = len(communities)
        current_time = timezone.now()
        context = {
            'communities': communities,
            'form': form,  # Pass the form to the template
            'number_of_created_communities': number_of_created_communities,
            'current_time': current_time,
        }
        return render(request, 'socio/createdcommunities.html', context)    

class AllCommunitiesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.all().order_by('-createdDate')
        form = CommunityForm()  
        communities_count = len(communities)
        current_time = timezone.now()
        context = {
            'communities': communities,
            'communities_count': communities_count,
            'current_time': current_time,
        }
        return render(request, 'socio/allcommunities.html', context)


class JoinCommunityView(LoginRequiredMixin, View):
    def get(self, request, community_id, *args, **kwargs):
        community = Community.objects.get(id=community_id)
        
        if community.is_private:

            messages.info(request, "You've sent a join request to the community owner.")
            return redirect('community_detail', community_id=community.id)  
        else:

            community.followers.add(request.user)
            messages.success(request, "You've successfully joined the community!")
            return redirect('community_detail', community_id=community.id) 

def home(request):

    communities = Community.objects.all().order_by('-createdDate')

    return render(request, 'socio/home.html', {'communities': communities})


@login_required
def create_post(request, community_id):
    community = Community.objects.get(id=community_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            community.posts.add(post)
            messages.success(request, 'Post creation successful.')
            return redirect('community_detail', community_id=community.id)
    else:
        form = PostForm()
    return render(request, 'socio/create_post.html', {'form': form})

@login_required
def community_detail(request, community_id):
    community = Community.objects.get(id=community_id)
    posts = community.posts.all().order_by('-created_at')
    return render(request, 'socio/community_detail.html', {'community': community, 'posts': posts})

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likers.all():
        post.likers.remove(request.user)
    else:
        post.likers.add(request.user)
        post.dislikers.remove(request.user) 
    return redirect('post_detail', post_id=post_id)

@login_required
def dislike_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.dislikers.all():
        post.dislikers.remove(request.user)
    else:
        post.dislikers.add(request.user)
        post.likers.remove(request.user)  
    return redirect('post_detail', post_id=post_id)


def community_detail(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    return render(request, 'socio/community_detail.html', {'community': community})

