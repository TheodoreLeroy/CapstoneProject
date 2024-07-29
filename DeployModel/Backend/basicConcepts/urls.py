from django.urls import path
from . import views

urlpatterns = [   

    # User
    path("students/", views.StudentList.as_view(), name="user-list"),

    # Class
    path("addClass/", views.ClassListCreate.as_view(), name='add-class'),
    path('classes/', views.ClassListCreate.as_view(), name='class-list'),
    path('classes/delete', views.ClassDelete.as_view(), name='delete-class'),

    # Slot
    path('class<int:classId>/', views.SlotInfomation.as_view(), name="create-slot"),
    path("slot/", views.SlotInfomation.as_view(), name="slot-information"),
]