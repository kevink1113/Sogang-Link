from django.contrib import admin
from . import models

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('major', 'course_id', 'name', 'advisor', 'classroom', 'semester')

