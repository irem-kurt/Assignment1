from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from community.models import Community, UserProfile
from . import views

# Create your views here.


class Index(View):
    def get(self, request, *args, **kwargs):
        communities = Community.objects.all().order_by('created_date')
        communities_count = len(communities)
        #currentTime = timezone.now()
        context = {
            'communities': communities,
            'communities_count': communities_count,
            #'currentTime': currentTime,
        }

        return render(request, 'commansys\index.html', context)

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        followers = profile.followers.all()
        #ratings_average = UserRatings.objects.filter(rated=profile.user).aggregate(Avg('rating'))
        if len(followers) == 0:
            is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        number_of_followers = len(followers)
        commmunities = Community.objects.filter(creater=profile.user)
        number_of_commmunities = len(commmunities)
        #posts = Post.objects.filter(eventcreater=profile.user)
        #number_of_posts = len(posts)
        #comments = UserRatings.objects.filter(rated=profile.user)
        context = {
            'user': user,
            'profile': profile,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
            #'ratings_average': ratings_average,
            #'comments': comments,
            'commmunities': commmunities,
            'number_of_commmunities': number_of_commmunities,
            #'posts': posts,
            #'number_of_posts': number_of_posts,
        }
        return render(request, 'commansys/profile.html', context)

#def base(request):

    #return HttpResponse("Hello, world. You're at the homepage.")


def community(request):

    return HttpResponse("Hello, world. You're at the community index.")



def user(request):

    return HttpResponse("Hello, world. You're at the user index.")


'''class Index(View):
    def get(self, request, *args, **kwargs):
        communities = community.objects.all().order_by('-createddate')
        communities_count = len(communities)
        currentTime = timezone.now()
        context = {
            'communities': communities,
            'communities_count': communities_count,
            'currentTime': currentTime,
        }

        return render(request, 'commansys/base.html', context)
'''