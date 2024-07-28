# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path("user/", views.StudentList.as_view(), name="user-list"),
    path("slot/", views.SlotInfomation.as_view(), name="slot-information"),
]