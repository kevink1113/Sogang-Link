# serializers.py
from rest_framework import serializers
from .models import Post, Comment
from users.models import User

class PostSerializer(serializers.ModelSerializer):
    sum_votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['id', 'title', 'content', 'created_at', 'author', 'view_count', 'sum_votes']


    def get_sum_votes(self, obj):
        # Calculate net votes: upvotes - downvotes
        return obj.upvotes.count() - obj.downvotes.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
