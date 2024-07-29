# users/urls.py
from django.urls import path
from . import views

urlpatterns = [   
    path("user/", views.StudentList.as_view(), name="user-list"),
    path("slot/", views.SlotInfomation.as_view(), name="slot-information"),
    path("addClass/", views.ClassListCreate.as_view(), name='add-class'),
    path('classes/', views.ClassListView.as_view(), name='class-list'),
]