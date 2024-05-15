from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassroomListView, BuildingInfoListView, MenuListView, RestaurantViewSet, TagViewSet

router = DefaultRouter(trailing_slash=False)
# router.register(r'maps', CourseViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('takes', StudentTakesListView.as_view(), name='student-takes-list'),
    # path('takes/<int:semester>', SemesterTakesListView.as_view(), name='semester-takes-list'),
    path('classroom', ClassroomListView.as_view(), name='classroom-list'),
    path('building', BuildingInfoListView.as_view(), name='building-list'),
    path('menus', MenuListView.as_view(), name='menu-list'),
    path('restaurants', RestaurantViewSet.as_view({'get': 'list'}), name='restaurant-list'), 
]
