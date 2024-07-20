# serializers.py
from rest_framework import serializers
from .models import Post, PostImage, Comment
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'nickname']

class PostSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    sum_votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', 'nickname', 'view_count', 'sum_votes']

    def get_nickname(self, obj):
        return obj.author.nickname if obj.author.nickname else obj.author.name

    def get_sum_votes(self, obj):
        return obj.upvotes.count() - obj.downvotes.count()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.query_params.get('anonymous') == 'true':
            ret.pop('author', None)
        return ret


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'author', 'nickname']

    def get_nickname(self, obj):
        # Optionally return the nickname if it exists, otherwise return an empty string
        return obj.author.nickname if obj.author.nickname else obj.author.name

    def to_representation(self, instance):
        # Custom representation to potentially exclude the author field
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.query_params.get('anonymous') == 'true':
            ret.pop('author', None)  # Remove the author field when anonymity is requested
        return ret
