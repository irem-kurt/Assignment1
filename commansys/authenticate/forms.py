from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import PasswordInput, TextInput
from .models import Profile, models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password'}))
    
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return password2
    



class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture'] 

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['location'].widget.attrs.update({'placeholder': 'Enter your location'})
        self.fields['birth_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
