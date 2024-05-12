from django.db import models
from users.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='posts')
    # mod = models.IntegerField(null=True)
    board = models.CharField(max_length=100, default='free')
    image = models.ImageField(upload_to='post_pictures/', null=True, blank=True)

    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)
    view_count = models.IntegerField(default=0, null=True, blank=True)
    
    def delete_post(self):
        self.delete()


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def delete_comment(self):
        self.delete()
