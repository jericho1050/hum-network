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