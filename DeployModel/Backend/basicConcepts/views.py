from rest_framework import generics

from .models import *
from .serializers import *


# CLASS
# get list class - urls: "class/"
# create new class- urls: "addClass/"
class ClassListCreate(generics.ListCreateAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):

        return Class.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
# get list class - urls: "class/delete" - not done
class ClassDelete(generics.DestroyAPIView):
    serializer_class = ClassSerializer

    def delete_queryset(self):
        id = self.request.id
        return Class.objects.filter(id=id)


# STUDENTS
# get list student - urls: "students/"
class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        return Student.objects.all()

# SLOT
# get slot-infomation - url: "slot/"
# post create-slot - url: "class=<int:classId>/"
class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)