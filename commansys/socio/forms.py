from django import forms

from .models import Community, Post, Comment

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
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'link']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': '4'})
        self.fields['link'].widget.attrs.update({'class': 'form-control'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':2}),
        }
