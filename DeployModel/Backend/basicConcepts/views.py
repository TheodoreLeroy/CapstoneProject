from .forms import ClassForm
from django.shortcuts import render, redirect
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from datetime import datetime, timedelta
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

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
            class_instance = serializer.save()
            # Create directory for the new class instance
            directory_path = 'Data/classes/' + str(class_instance.class_name)
            if(not os.path.exists(directory_path)):
                os.makedirs(directory_path, exist_ok=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        class_id = self.kwargs.get('classId')
        if not class_id:
            return Response({'error': 'Class ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            class_instance = Class.objects.get(id=class_id)
            # Delete directory for the class instance
            directory_path = directory_path = 'Data/classes/' + \
                str(class_instance.class_name)
            if os.path.exists(directory_path):
                os.rmdir(directory_path)
            class_instance.delete()
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

# STUDENTS
# get list student - urls: "students/"


class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Student.objects.filter(class_id_id=id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


# get list student - urls: "studentsClass<int:classId>/"
class StudentFromClassId(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        class_id = self.kwargs.get('classId')
        return Student.objects.filter(class_id_id=class_id)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                student = serializer.save()
                if 'image' in request.FILES:
                    image = Image.open(request.FILES['image'])
                    max_width, max_height = 300, 300  # Desired size

                    # Resize the image while maintaining aspect ratio
                    image.thumbnail((max_width, max_height), Image.LANCZOS)
                    img_io = BytesIO()
                    image.save(img_io, format='JPEG')
                    student.image.save(student.image.name, ContentFile(
                        img_io.getvalue()), save=False)
                    student.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error: {e}")
        return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            student_id = self.kwargs.get('pk')
            student = Student.objects.get(pk=student_id)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            raise NotFound(detail="Student not found",
                           code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# SLOT
# get slot-infomation - url: "slot/"
# post create-slot - url: "class=<int:classId>/createSlot"


class SlotInformation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    def delete(self, request, *args, **kwargs):
        slot_id = self.kwargs.get('slotId')
        if not slot_id:
            return Response({'error': 'Class ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot_instance = Slot.objects.get(id=slot_id)
            slot_instance.delete()
            return Response({'message': 'Class deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Slot.DoesNotExist:
            return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)


# Get slot-information for 1 class with class_id - url: "class<int:classId>/slot/"


class SlotInformationFromIdClass(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('classId')
        return Slot.objects.filter(class_id=id)

# Get 1 slot-information with id - url: "slot<int:slotId>/"


class SlotInformationFromId(generics.ListCreateAPIView):
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
