# users/urls.py
from django.urls import path
from . import views as v

urlpatterns = [   
    path("user/", v.StudentList.as_view(), name="user-list"),
    path("slot/", v.SlotInfomation.as_view(), name="slot-information"),
    path('add_class/', v.AddClass.add_class, name='add-class'),
    path('classes/', v.ClassListView.as_view(), name='class-list'),
]