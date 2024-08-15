import cv2
# from .forms import ClassForm
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
import requests
import torch
import threading
import time
from datetime import datetime, timedelta
from torchvision import models, transforms
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

            os.makedirs(directory_path + '/embedding', exist_ok=True)
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


def handleFilePath(file_path):
    file_path_str = str(file_path)
    path_components = file_path_str.split('/')

    # new_component = 'students'
    # path_components.insert(-1, new_component)

    name, ext = os.path.splitext(path_components[-1])

    new_file_name = name + '.txt'
    path_components.append(new_file_name)

    new_file_path = '/'.join(path_components)
    return new_file_path

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

    # Convert image to embedding type

    def create(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                class_instance = Class.objects.get(
                    id=validated_data['class_id'].id)
                student = Student(
                    class_id=validated_data['class_id'],
                    name=validated_data['name'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )
                os.makedirs
                student.save()
                print(serializer)
                if 'image' in request.FILES:
                    image = Image.open(request.FILES['image'])
                    max_width, max_height = 300, 300  # Desired size
                    # Resize the image while maintaining aspect ratio
                    image.thumbnail((max_width, max_height), Image.LANCZOS)

                    # Convert the image to RGB mode if it has an alpha channel
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    img_io = BytesIO()
                    image.save(img_io, format='JPEG')
                    # print(class_instance.class_name)
                    print("break1")
                    file_path = f'Data/classes/{class_instance.class_name}/students/{student.student_id}_{student.name}'
                    directory = os.path.dirname(
                        file_path + f'/{student.student_id}_{student.name}')
                    if not os.path.exists(directory):
                        os.makedirs(directory, exist_ok=True)
                    image.save(
                        file_path + f'/{student.student_id}_{student.name}.jpg', format='JPEG')

                    print("break")
                    student.image = file_path
                    student.save()
                    print("first path" + str(student.image))

                    image_path = str(student.image)
                    print("image path:" + image_path)
                    file_path = handleFilePath(image_path)
                    print("file path:" + file_path)

                    # Send image to external API
                    data = ProcessImageData(
                        image_path + f'/{student.student_id}_{student.name}.jpg')
                    with open(file_path, 'w') as file:
                        for vector in data['embeddings']:
                            vector_str = ' '.join(map(str, vector))
                            file.write(f'{vector_str}\n')

                # Add id field to data
                respone_data = serializer.data
                respone_data['ID'] = student.student_id
                print(respone_data)
                return Response(respone_data, status=status.HTTP_201_CREATED)
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

# API - source model2 - Phuc
# url: http://127.0.0.1:5001/process_image


def ProcessImageData(path):
    with open(path, 'rb') as image_file:
        files = {
            "image": ("test_image.jpg", image_file, "image/jpeg")}
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)
        if response.status_code == 200:
            print("API request success")
            return response.json()
        else:
            return response.Response({'error': 'Failed to process image'}, status=response.status_code)


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

# class RunCameraInSlot(generics.ListCreateAPIView):


# Process image api
class ProcessImageView(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        # Get the image from the request
        image = request.FILES.get('image')

        if not image:
            return JsonResponse({'error': 'No image provided'}, status=400)

        # Prepare the files for the API request
        files = {'image': (image.name, image, image.content_type)}

        # Send the request to the external API
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)

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


# Connect to camera


class CameraHandle(generics.ListCreateAPIView):
    serializer_class = CameraInfor

# def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     # 0 is the default camera
#     self.cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
#     self.running = True
#     self.snapshot_thread = threading.Thread(target=self.take_snapshots)
#     self.snapshot_thread.start()

# def take_snapshots(self):
#     next_snapshot_time = datetime.now() + timedelta(seconds=30)
#     while self.running:
#         ret, frame = self.cap.read()
#         if ret:
#             cv2.imshow('Frame', frame)
#             if datetime.now() >= next_snapshot_time:
#                 timestamp = int(time.time())
#                 filename = f'snapshot_{timestamp}.jpg'
#                 cv2.imwrite(filename, frame)
#                 print(f"Snapshot saved as {filename}")
#                 next_snapshot_time = datetime.now() + timedelta(seconds=30)
#         if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
#             self.running = False
#             break
#     self.cap.release()
#     cv2.destroyAllWindows()

# def post(self, request, *args, **kwargs):
#     return JsonResponse({'status': 'Camera is running and taking snapshots every 10 minutes'})

# def destroy(self, request, *args, **kwargs):
#     self.running = False
#     self.snapshot_thread.join()
#     self.cap.release()
#     cv2.destroyAllWindows()
#     return JsonResponse({'status': 'Camera stopped'})

# def __del__(self):
#     self.running = False
#     self.snapshot_thread.join()
#     self.cap.release()
#     cv2.destroyAllWindows()

# __________________ HA DJANGO ___________________________

# add Class

# def test():
#     # Initialize the camera
#     cap = cv2.VideoCapture(0)  # 0 is the default camera
#     img_counter = 0
#     while True:
#         # Capture frame-by-frame
#         ret, frame = cap.read()
#         if not ret:
#             print("failed to grab frame")
#             break
#         # Display the resulting frame
#         cv2.imshow('frame', frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             print("Quitting")
#             break
#         elif cv2.waitKey(1) & 0xFF == ord(' '):
#             img_name = "myPic_{}.png".format(img_counter)
#             cv2.imwrite(img_name, frame)
#             print("{} written".format(img_name))
#             img_counter += 1

#     # Release the capture and close the window
#     cap.release()
#     cv2.destroyAllWindows()


def post():
    # Get the image from the request
    # image = request.FILES.get('image')

    # if not image:
    #     return JsonResponse({'error': 'No image provided'}, status=400)
    image_path = "myPic_0.png"

    with open(image_path, "rb") as image_file:
        files = {"image": ("test_image.jpg", image_file, "image/jpeg")}
        # Send the request to the external API
        response = requests.post(
            'http://127.0.0.1:5001/process_image', files=files)

    if response.status_code == 200:
        print("API request successful")
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Failed to process image'}, status=response.status_code)


def test_and_draw():
    data = post()
    # Print the received data
    print("Received boxes:", data['boxes'])
    print("Received embeddings shape:", [len(emb)
          for emb in data['embeddings']])

    # image = cv2.imread("myPic_0.png")
    # draw = cv2.imshow("test", image)

    # for box in data['boxes']:
    #     x1, x2, y1, y2 = box
    #     draw.rectangle([x1, y1, x2, y2], outline="red", width=2)


# test()
# test_and_draw()
