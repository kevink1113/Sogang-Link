from django.db import models

# Create your models here.

class Notice(models.Model):
    board = models.CharField(max_length=100, null=True)   # 게시판
    title = models.CharField(max_length=100, null=True)   # 제목
    url = models.URLField(null=True)                      # 링크
    writer = models.CharField(max_length=100, null=True)  # 작성자
    date = models.DateTimeField(null=True)                    # 시간
    objects = models.Manager()