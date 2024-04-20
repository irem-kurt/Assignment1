from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import UserProfile

from django.contrib.auth import login
from .forms import CreateUserForm
from .models import UserProfile
from django.contrib import messages
from django.shortcuts import render, redirect

# - Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
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
    profile = get_object_or_404(UserProfile, id=id)

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
