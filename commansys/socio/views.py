from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

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

class PublicCommunityView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.filter(is_private=False)
        context = {
            'community': communities
        }
        return render(request, 'socio/community-view.html', context)

    
