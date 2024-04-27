from datetime import timezone
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.contrib import messages

from .forms import CommunityForm

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
            # If the community is private, send a request to join
            messages.info(request, "You've sent a join request to the community owner.")
            return redirect('community_detail', community_id=community.id)  # Redirect to community detail page
        else:
            # If the community is public, add the user to the community
            community.followers.add(request.user)
            messages.success(request, "You've successfully joined the community!")
            return redirect('community_detail', community_id=community.id)  # Redirect to community detail page

def home(request):
    return render(request, 'socio/home.html')