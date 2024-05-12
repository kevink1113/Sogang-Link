# urls.py
from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, toggle_upvote, toggle_downvote


urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:pk>/upvote', toggle_upvote, name='post-upvote'),
    path('<int:pk>/downvote', toggle_downvote, name='post-downvote'),
]
