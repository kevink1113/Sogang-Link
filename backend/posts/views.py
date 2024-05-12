from .permissions import IsAuthorOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import F



class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['board','author', 'title', 'content']
    ordering_fields = ['created_at', 'upvote_num', 'view_num']

    def get_queryset(self): # To reduce DB query
        return Post.objects.all().prefetch_related('upvotes', 'downvotes')

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self): # To reduce DB query
        return Post.objects.all().prefetch_related('upvotes', 'downvotes')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = F('view_count') + 1
        instance.save(update_fields=['view_count'])
        instance.refresh_from_db()
        return super().retrieve(request, *args, **kwargs)

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'author', 'content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

@api_view(['POST'])
@permission_classes([IsAuthorOrReadOnly])
def toggle_upvote(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
        voted = False
    else:
        post.upvotes.add(request.user)
        # Ensure a user cannot downvote and upvote the same post
        post.downvotes.remove(request.user)
        voted = True
    return Response({"voted": voted}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthorOrReadOnly])
def toggle_downvote(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)
        voted = False
    else:
        post.downvotes.add(request.user)
        # Ensure a user cannot upvote and downvote the same post
        post.upvotes.remove(request.user)
        voted = True
    return Response({"voted": voted}, status=status.HTTP_200_OK)