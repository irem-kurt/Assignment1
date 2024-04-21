
from .models import Profile
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.urls import reverse
from . forms import CreateUserForm, LoginForm, ProfileForm

from django.contrib.auth.decorators import login_required


from django.contrib.auth import login
from .forms import CreateUserForm

from django.contrib import messages
from django.shortcuts import render, redirect

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.views import View

def home(request):

    return render(request, 'authenticate/index.html')

class RegisterView(View):
    form_class = CreateUserForm
    initial = {'key': 'value'}
    template_name = 'authenticate/registerpage.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            #to do: goes to feed
            return redirect(to='/authenticate/home')

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

                return redirect("dashboard")


    context = {'loginform':form}

    return render(request, 'authenticate/my-login.html', context=context)


def user_logout(request):

    auth.logout(request)

    return redirect("/authenticate/")



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
        #'location': profile.location,
        #'picture': profile.picture,
        'followers': profile.followers.all(),
        'unreadcount': profile.unreadcount
    }

    # Render the user profile template with the context data
    return render(request, 'authenticate/user-profile.html', context)

'''
@login_required(login_url="my-login")
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    context = {"profiles": profiles}
    return render(request, '/authenticate/profile-list.html', context)
'''

'''
@login_required(login_url="my-login")
def view_profile(request):
    # Get the current user
    username = request.session['username']

    try:
        # Try to retrieve the user's profile
        user_profile = Profile.objects.get(email=username)
    except Profile.DoesNotExist:
        # If the profile does not exist, redirect to the edit profile page
        return redirect('edit_profile')
    print("user photo: " + str(user_profile.photo).split("'")[1])
    user_photo = "/media/" + str(user_profile.photo).split("'")[1]

    return render(request, 'profile.html', {'user_profile': user_profile, 'user_photo': user_photo})
'''
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required(login_url="my-login")
def view_profile(request, id):
    # Retrieve the UserProfile object or return a 404 error if not found
    profile = get_object_or_404(Profile, pk=id)

    # Prepare the context data to pass to the template
    context = {
        'profile': profile,
        'name': profile.name,
        'bio': profile.bio,
        'birth_date': profile.birth_date,
        # 'location': profile.location,
        # 'picture': profile.picture,
        'followers': profile.followers.all(),
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
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Save the form data to update the profile
            form.save()
            # Redirect to the profile detail page after successful update
            return redirect('user-profile', id=id)
    else:
        # Create a form instance with the instance of the profile to edit
        form = ProfileForm(instance=profile)

    # Render the edit profile template with the form
    return render(request, 'authenticate/edit-profile.html', {'form': form})
