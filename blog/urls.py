from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('create/', views.create_post, name='create-post'),
    path('update/<int:pk>/', views.update_post, name='update-post'),
    path('delete/<int:pk>/', views.delete_post, name='delete-post'),
    path('register/', views.register, name='register'),
    # path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('like/<int:pk>/', views.like_post, name='like-post'),
    path('favorite/<int:pk>/',views.toggle_favorite,name='toggle-favorite'),
    path('comment/<int:pk>/edit/',views.edit_comment,name='edit-comment'),
    path('comment/<int:pk>/delete/',views.delete_comment,name='delete-comment'),
]