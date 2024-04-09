from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        label = 'Name',
        widget = forms.Textarea(attrs={
            'rows': '1',
            'placeholder': 'Your name...'
        })
    )
    
    bio = forms.CharField(
        label = 'Bio',
        widget = forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Your bio...'
        })
    )


    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'birth_date', 'location', 'picture']