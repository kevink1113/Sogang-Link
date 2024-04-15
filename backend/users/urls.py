# urls.py in your users app

from django.urls import path
from .views import UpdateUserInfoView, UpdateTakesView, UpdateGradesView, UserInfoView

urlpatterns = [
    path('info', UserInfoView.as_view(), name='user-info'),
    path('update_user_info', UpdateUserInfoView.as_view(), name='update_user_info'),
    path('update_takes', UpdateTakesView.as_view(), name='manage_takes'),
    path('update_grades', UpdateGradesView.as_view(), name='manage_grades'),
]
