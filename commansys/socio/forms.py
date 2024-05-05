from django import forms
from .models import Community, Comment, PostTemplateItem, PostTemplateItemType


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

    rules = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': '5',
            'placeholder': 'Set the rules of the community here'
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
        fields = ['name', 'description', 'rules', 'picture', 'location', 'is_private']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
          'text': forms.Textarea(attrs={'rows':2}),
        }
        
        
class PostTemplateItemForm(forms.ModelForm):
    class Meta:
        model = PostTemplateItem
        fields = ['name', 'post_type', 'mandatory']

    def __init__(self, *args, **kwargs):
        super(PostTemplateItemForm, self).__init__(*args, **kwargs)
        self.fields['post_type'].widget = forms.Select(choices=PostTemplateItemType.choices())
        
        
class DefaultPostForm(forms.Form):
    title = forms.CharField(label='Title *', max_length=100)
    description = forms.CharField(label='Description (optional)', widget=forms.Textarea(attrs={'rows': 5}), required=False)
