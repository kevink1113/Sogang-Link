from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Post)

class CommentsInline(admin.TabularInline):
    model = models.Comment
    extra = 1

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentsInline]
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
  

# # @admin.register(models.Course)
# # class CourseAdmin(admin.ModelAdmin):
# #     search_fields = ['major', 'course_id', 'name', 'advisor', 'classroom', 'semester']
# #     list_display = ('major', 'course_id', 'name', 'advisor', 'classroom', 'semester')


# # class TakesInline(admin.TabularInline):
# #     model = models.Takes
# #     readonly_fields = ('course_name', 'semester', 'middle_grade', 'final_grade')
# #     extra = 1  # Specifies the number of blank forms the formset should display.

# #     def course_name(self, obj):
# #         return obj.course.name
# #     course_name.short_description = '과목명'

# #     def semester(self, obj):
# #         return obj.course.semester
# #     semester.short_description = '학기'

