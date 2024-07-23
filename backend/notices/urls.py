from django.contrib import admin
from django.urls  import path, include
from . import views

urlpatterns = [
  path('notify_topic', views.notify_topic),
]