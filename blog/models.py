from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField  # ← add this import


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    image = CloudinaryField(
        'image',
        folder='posts/',       # organizes uploads in your Cloudinary dashboard
        blank=True,
        null=True
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    
    favorites = models.ManyToManyField(
        User,
        related_name='favorite_posts',
        blank=True
    )

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = CloudinaryField(
        'image',
        folder='profile_pics/',
        default='default.jpg',   # Cloudinary will look for this in your media library
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user} ❤️ {self.post.title}"

class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"