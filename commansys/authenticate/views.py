
from .models import Profile
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, ProfileForm

from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm

from django.contrib import messages
from django.shortcuts import render, redirect

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
            user = form.save()

            '''user_profile = Profile(user=user, id=user.id)
            user_profile.save()'''

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
