from django import forms

from .models import User, Post, Likes, Follow

class UserProfilePicForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='', widget=forms.FileInput(attrs={'class': 'profile-pic-input'}))

    class Meta:
        model = User
        fields = ["profile_picture"]
        exclude  = []

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            'content': forms.Textarea(attrs={'class': 'textarea', 'placeholder': "What's on your mind? Post something here."}),
        }
        exclude = [ ]
        
class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': "What's happening?",
            # Basic character counter example (can be enhanced with JS/HTMX extensions)
            'oninput': "document.getElementById('char-count').innerText = this.value.length;"
        }),
        label="" # Hide the default label
    )

    class Meta:
        model = Post
        fields = ['content']
