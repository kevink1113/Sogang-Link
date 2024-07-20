from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView, toggle_upvote, toggle_downvote, PostSearchListView, UploadPostImages  # 클래스 이름을 가져옵니다.

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comments', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:pk>/upvote', toggle_upvote, name='post-upvote'),
    path('<int:pk>/downvote', toggle_downvote, name='post-downvote'),
    path('search', PostSearchListView.as_view(), name='search-posts'),
    path('<int:post_id>/upload-images', UploadPostImages.as_view(), name='upload-images'),  # 여기서 .as_view()를 호출합니다.
]