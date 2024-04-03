from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from .views import StudentTakesListView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('takes', StudentTakesListView.as_view(), name='student-takes-list'),
]