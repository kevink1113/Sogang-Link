from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
from .views import StudentTakesListView, SemesterTakesListView

router = DefaultRouter(trailing_slash=False)
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('takes', StudentTakesListView.as_view(), name='student-takes-list'),
    path('takes/<int:pk>', StudentTakesListView.as_view(), name='takes-detail'),  # Handle PUT and DELETE
    path('takes/<int:semester>', SemesterTakesListView.as_view(), name='semester-takes-list'),
]
