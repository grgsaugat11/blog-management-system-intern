from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from .models import Post, Profile, Favorite, Comment, Activity
from .forms import (
    PostForm,
    CommentForm,
    UserRegisterForm,
    ProfileUpdateForm
)


# ================= HOME =================

def home(request):

    query = request.GET.get('q')

    posts = Post.objects.all().order_by('-created_at')

    if query:

        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        )

    context = {
        'posts': posts,
        'query': query
    }

    return render(request, 'blog/home.html', context)


# ================= POST DETAIL =================

def post_detail(request, pk):

    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.all()

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():

                comment = form.save(commit=False)

                comment.post = post
                comment.user = request.user

                comment.save()
                Activity.objects.create(
                    user=request.user,
                    action=f"Commented on: {post.title}"
                )

                return redirect('post-detail', pk=pk)

    else:

        form = CommentForm()

    return render(request, 'blog/post_detail.html', {

        'post': post,
        'comments': comments,
        'form': form

    })

# ================= FAVORITE POST =================

@login_required
def toggle_favorite(request, pk):

    post = get_object_or_404(Post, pk=pk)

    favorite = Favorite.objects.filter(
        user=request.user,
        post=post
    )

    if favorite.exists():

        favorite.delete()

        favorited = False

    else:

        Favorite.objects.create(
            user=request.user,
            post=post
        )

        favorited = True

    return JsonResponse({
        'favorited': favorited
    })

# ================= CREATE POST =================

@login_required
def create_post(request):

    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()
            Activity.objects.create(
                user=request.user,
                action=f"Created a post: {post.title}"
            )

            return redirect('home')

    else:

        form = PostForm()

    return render(request, 'blog/post_form.html', {

        'form': form

    })


# ================= UPDATE POST =================

@login_required
def update_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:

        return redirect('home')

    if request.method == 'POST':

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            return redirect('post-detail', pk=pk)

    else:

        form = PostForm(instance=post)

    return render(request, 'blog/post_form.html', {

        'form': form

    })


# ================= DELETE POST =================

@login_required
def delete_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:

        post.delete()

    return redirect('home')

# ================= EDIT COMMENT =================

@login_required
def edit_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    # only comment owner can edit
    if request.user != comment.user:
        return redirect('home')

    if request.method == 'POST':

        form = CommentForm(
            request.POST,
            instance=comment
        )

        if form.is_valid():

            form.save()

            Activity.objects.create(
                user=request.user,
                action=f"Edited a comment on: {comment.post.title}"
            )

            return redirect(
                'post-detail',
                pk=comment.post.pk
            )

    else:

        form = CommentForm(instance=comment)

    return render(
        request,
        'blog/edit_comment.html',
        {
            'form': form,
            'comment': comment
        }
    )

# ================= DELETE COMMENT =================

@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if request.user == comment.user:

        Activity.objects.create(
            user=request.user,
            action=f"Deleted a comment on: {comment.post.title}"
        )

        post_pk = comment.post.pk

        comment.delete()

        return redirect(
            'post-detail',
            pk=post_pk
        )

    return redirect('home')

# ================= LIKE POST =================

@login_required
def like_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

        liked = False

    else:

        post.likes.add(request.user)

        liked = True
        Activity.objects.create(
            user=request.user,
            action=f"Liked post: {post.title}"
        )

    return JsonResponse({

        'liked': liked,
        'likes_count': post.likes.count()

    })


# ================= PROFILE =================

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.filter(
        author=request.user
    ).order_by('-created_at')

    total_likes = 0

    for post in posts:

        total_likes += post.likes.count()

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile,
            user=request.user
        )

        if form.is_valid():

            form.save(user=request.user)

            messages.success(
                request,
                'Profile updated successfully!'
            )

            return redirect('profile')

    else:

        form = ProfileUpdateForm(
            instance=profile,
            user=request.user
        )
    
    favorites = Favorite.objects.filter(
        user=request.user
    )
    
    activities = Activity.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    return render(request, 'blog/profile.html', {

        'form': form,
        'posts': posts,
        'total_posts': posts.count(),
        'total_likes': total_likes,
        'favorites': favorites,
        'activities': activities

    })


# ================= REGISTER =================

def register(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            return redirect('home')

    else:

        form = UserRegisterForm()

    return render(request, 'blog/register.html', {

        'form': form

    })