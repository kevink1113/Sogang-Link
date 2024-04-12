from django.contrib import admin
from . import models

@admin.register(models.Notice)
class NoticeAdmin(admin.ModelAdmin):
    search_fields = ('board', 'title', 'url', 'writer', 'date')
    list_display = ('title', 'board', 'writer', 'date')
    list_filter = ('board', 'writer', 'date')
    # ordering = ('-date',)