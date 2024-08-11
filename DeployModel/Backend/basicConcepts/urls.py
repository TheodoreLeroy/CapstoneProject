from django.urls import path
from . import views

urlpatterns = [   

    # User
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("studentsClass<int:classId>/", views.StudentFromClassId.as_view(), name="student-list-from-class-id"),
    
    # Class
    path("addClass/", views.ClassView.as_view(), name='add-class'),
    path('classes/', views.ClassView.as_view(), name='class-list'),
    path('class<int:classId>/', views.ClassView.as_view(), name="get-one-class"),
    path('classes/detail', views.ClassView.as_view(), name='get-detail-class'),

    # Slot
    path('class<int:classId>/createSlot', views.SlotInfomation.as_view(), name="create-slot"),
    path("slot/", views.SlotInfomation.as_view(), name="slot-information"),
    path("class<int:classId>/slot/", views.SlotInfomationFromIdClass.as_view(), name="slot-information-from-one-class"),
    path("slot<int:slotId>/", views.SlotInfomationFromId.as_view(), name="one-slot-information"),

    # Log
    path("slot<int:slotId>/timeFrame/", views.GetTimeFrame.as_view(), name="time-frames-of-slot"),
    path("timeFrame<int:timeFrameId>/", views.GetAttendentStudentsAtOneFrame.as_view(), name="a-time-frames-of-slot"),
    #attentdent
    # path("class<int:classId>/slot<int:classId>/", views.SlotInfomationFromIdClass.as_view(), name="slot-information-from-one-class"),
]