from django.urls  import path
from .views import notify_topic

urlpatterns = [
  path('notify_topic', notify_topic, name='notify_topic'),
]