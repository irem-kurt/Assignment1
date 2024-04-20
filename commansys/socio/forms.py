from django import forms

from .models import Community

class CommunityForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Community Name...'
        })
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '3',
            'placeholder': 'Community Description...'
        })
    )
    
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'form-control-file'
        })
    )

    location = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Location...'
        })
    )

    is_private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    class Meta:
        model = Community
        fields = ['name', 'description', 'picture', 'location', 'is_private']
        
        
