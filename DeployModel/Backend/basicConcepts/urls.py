from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Student url
    path("students/<int:classId>/",
         views.StudentList.as_view(), name="student-list"),
    #     path("studentsadd/", views.StudentList.as_view(), name="student-add"),
    path("addStudent/<int:classId>/", views.StudentFromClassId.as_view(),
         name="add_student_to_class"),
    # Delete student
    path('students/<int:classId>/<int:pk>/',
         views.StudentFromClassId.as_view(), name='student-detail-destroy'),
    #     path("studentsClass<int:classId>/", views.StudentFromClassId.as_view(),
    #          name="student-list-from-class-id"),

    # Class url
    # Render home page with classes
    path('classes/detail', views.ClassView.as_view(), name='get-detail-class'),
    # Create class
    path("addClass/", views.ClassView.as_view(), name='add-class'),
    # Delete class
    path('deleteClass/<int:classId>/',
         views.ClassView.as_view(), name='delete_class'),
    path('classes/', views.ClassView.as_view(), name='class-list'),
    path('classes/<int:classId>/', views.ClassView.as_view(), name="get-one-class"),



    # Slot url
    # Render internal infor of class
    path('classes/<int:classId>', views.SlotInformation.as_view(), name='index'),
    # Create slot
    path('classes/<int:classId>/createSlot',
         views.SlotInformation.as_view(), name="create-slot"),
    # Delete slot
    path('deleteSlot/<int:slotId>/',
         views.SlotInformation.as_view(), name='delete_slot'),


    path("slot/", views.SlotInformation.as_view(), name="slot-information"),
    path("classes/<int:classId>/slot/", views.SlotInformationFromIdClass.as_view(),
         name="slot-information-from-one-class"),
    path("slot<int:slotId>/", views.SlotInformationFromId.as_view(),
         name="one-slot-information"),
    path("slot/camera/",
         views.CameraHandle.as_view(), name="camera_on"),


    # Log
    path("slot<int:slotId>/timeFrame/",
         views.GetTimeFrame.as_view(), name="time-frames-of-slot"),
    path("timeFrame<int:timeFrameId>/",
         views.GetAttendentAtOneFrame.as_view(), name="a-time-frames-of-slot"),
    # attentdent
    # path("class<int:classId>/slot<int:classId>/", views.SlotInfomationFromIdClass.as_view(), name="slot-information-from-one-class"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
