from django.urls import path
from .views import PostListCreateView, PostDetailView

urlpatterns = [
    # URL for listing all posts or creating a new post
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),

    # URL for retrieving, updating, or deleting a single post
    path('posts/<int:post_id>', PostDetailView.as_view(), name='post-detail'),
]
