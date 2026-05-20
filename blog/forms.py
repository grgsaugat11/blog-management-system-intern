from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):

    image = forms.ImageField(
        label="Change Image",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    remove_image = forms.BooleanField(
        required=False,
        label="Remove current image"
    )

    class Meta:
        model = Post
        fields = ['title', 'image', 'content']

    def save(self, commit=True):

        post = super().save(commit=False)

        if self.cleaned_data.get('remove_image'):
            post.image.delete(save=False)
            post.image = None

        if commit:
            post.save()

        return post


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']


class ProfileUpdateForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )

    image = forms.ImageField(
        label="Change Image",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    remove_image = forms.BooleanField(
        required=False,
        label="Remove current image"
    )

    class Meta:
        model = Profile
        fields = ['image', 'bio']

    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:
            self.fields['username'].initial = user.username

    def save(self, user=None, commit=True):

        profile = super().save(commit=False)

        if self.cleaned_data.get('remove_image'):
            profile.image.delete(save=False)
            profile.image = None

        if user:
            user.username = self.cleaned_data['username']
            user.save()

        if commit:
            profile.save()

        return profile

    image = forms.ImageField(
        label="Change Profile Picture",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Profile
        fields = ['image', 'bio']