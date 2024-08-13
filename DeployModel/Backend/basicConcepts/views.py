from .forms import ClassForm
from django.shortcuts import render, redirect
from rest_framework import generics

from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta

# CLASS
# get list class - url: "class/"
# create new class- url: "addClass/"
# get list class that have id - url: "classes/detail/"
# get 1 class with id of that class - url:


class ClassView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        # Use the appropriate serializer based on the type of request
        if 'classId' in self.kwargs or self.request.path.endswith('detail'):
            return ClassDetailSerializer
        return ClassSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('classId')
        if class_id:
            return Class.objects.filter(id=class_id)
        return Class.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        class_id = self.kwargs.get('classId')
        if not class_id:
            return Response({'error': 'Class ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            class_instance = Class.objects.get(id=class_id)
            class_instance.delete()
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

# STUDENTS
# get list student - urls: "students/"


class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        return Student.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


# get list student - urls: "studentsClass<int:classId>/"
class StudentFromClassId(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Student.objects.filter(class_id=id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

# SLOT
# get slot-infomation - url: "slot/"
# post create-slot - url: "class=<int:classId>/createSlot"


class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

# Get slot-information for 1 class with class_id - url: "class<int:classId>/slot/"


class SlotInfomationFromIdClass(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Slot.objects.filter(class_id=id)

# Get 1 slot-information with id - url: "slot<int:slotId>/"


class SlotInfomationFromId(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return Slot.objects.filter(id=id)


class GetTimeFrame(generics.ListCreateAPIView):
    serializer_class = TimeFrameSerializer

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return TimeFrame.objects.filter(slot_id=id)


class GetAttendentStudentsAtOneFrame(generics.ListCreateAPIView):
    serializer_class = AttendentStudentsAtOneFrameSerializer

    def get_queryset(self):
        timeFrameId = self.kwargs.get('timeFrameId')
        return AttendentStudentsAtOneFrame.objects.filter(time_frame=timeFrameId)


# __________________ HA DJANGO ___________________________


# add Class

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()
    return render(request, 'add_class.html', {'form': form})
