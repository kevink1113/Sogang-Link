from django.contrib import admin
from lecture.admin import TakesInline
from . import models


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [TakesInline]
