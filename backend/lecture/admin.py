from django.contrib import admin
from . import models

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['major', 'course_id', 'name', 'advisor', 'classroom', 'semester']
    list_display = ('major', 'course_id', 'name', 'advisor', 'classroom', 'semester')
