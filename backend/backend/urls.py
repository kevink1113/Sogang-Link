"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from backend import settings
from backend.views import offline, my_login_view

from .views import LoginView, ChatView
from notices.views import NoticeViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Sogang Link API",
        default_version='v1',
        description="Sogang Link를 위한 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="me@kevink1113.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(), name='login'),
    path('chat', ChatView.as_view(), name='chat'),
    # path('stream', StreamView.as_view(), name='stream'),
    # path('login/', my_login_view, name='my_login_view'),
    path('offline/', offline, name='offline'),
    path('users/', include('users.urls')),
    path('lecture/', include('lecture.urls')),
    path('notice', NoticeViewSet.as_view(), name='notice'),
    path('maps/', include('maps.urls')),
    path('posts/', include('posts.urls')),
    path('notices/', include('notices.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]
