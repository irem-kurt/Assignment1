
from django.http import HttpResponseRedirect, JsonResponse
from .models import Profile
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from django.contrib.auth.models import User

from . forms import CreateUserForm, LoginForm, ProfileForm

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

from django.contrib import messages
from django.shortcuts import render, redirect

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.views import View
from .views import login

class RegisterView(View):
    template_name = 'authenticate/registerpage.html'

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            user_profile = Profile(user=user, id=user.id, name=form.cleaned_data.get('name'))
            user_profile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            if user is not None:
                return redirect('my-login')

        return render(request, self.template_name, {'form': form})


def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('home')


    context = {'loginform':form}

    return render(request, 'authenticate/my-login.html', context=context)


def user_logout(request):
    auth.logout(request)
    return redirect(reverse('home'))


@login_required(login_url="my-login")
def dashboard(request):

    return render(request, 'authenticate/dashboard.html')


@login_required(login_url="my-login")
def user_profile(request, id):
    # Retrieve the UserProfile object or return a 404 error if not found
    profile = get_object_or_404(Profile, pk=id)

    # Prepare the context data to pass to the template
    context = {
        'profile': profile,
        'name': profile.name,
        'bio': profile.bio,
        'birth_date': profile.birth_date,
        'location': profile.location,
        'picture': profile.picture,
        'followers': profile.followers.all(),
        'unreadcount': profile.unreadcount
    }

    # Render the user profile template with the context data
    return render(request, 'authenticate/user-profile.html', context)

'''
from django.contrib.auth.models import User
def create_user_and_profile(request):
    # Create a new user
    user = User.objects.create(username='example_user', email='user@example.com')
    
    # Create a profile for the user
    profile = Profile.objects.create(
        user=user,
        name='Example User',
        bio='This is a bio',
        birth_date=None,  # Set to whatever is appropriate
        location='41.0255493,28.9742571',  # Set to default location
        picture='example.jpg',  # Set to default picture
        unreadcount=0  # Set to default unread count
    )
    return render(request, 'authenticate/user-profile.html', profile)
'''

@login_required(login_url="my-login")
def view_profile(request, id):
    # Retrieve the UserProfile object or return a 404 error if not found
    profile = get_object_or_404(Profile, pk=id)

    following = request.user in profile.followers.all()
    print(f'following {following} {profile.name} ${profile.followers.all()}')
    
    # Prepare the context data to pass to the template
    context = {
        'profile': profile,
        'name': profile.name,
        'bio': profile.bio,
        'birth_date': profile.birth_date,
        'location': profile.location,
        'picture': profile.picture,
        'followers': profile.followers.all(),
        'following': following,
        'unreadcount': profile.unreadcount
    }

    # Render the user profile template with the context data
    return render(request, 'authenticate/user-profile.html', context)

@login_required(login_url="my-login")
def edit_profile(request, id):
    # Retrieve the profile object to edit
    profile = get_object_or_404(Profile, pk=id)

    if request.method == 'POST':
        # Create a form instance with the POST data and the instance of the profile to edit
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form data to update the profile
            profile = form.save(commit=False)
            profile.user = request.user  # Associate the profile with the current user
            profile.save()
            print(f'Profile updated successfully : {profile.picture} : {profile.picture.url}')
            # Redirect to the profile detail page after successful update
            return redirect('user-profile', id=id)
    else:
        # Create a form instance with the instance of the profile to edit
        form = ProfileForm(instance=profile)

    # Render the edit profile template with the form
    return render(request, 'authenticate/edit-profile.html', {'form': form})
