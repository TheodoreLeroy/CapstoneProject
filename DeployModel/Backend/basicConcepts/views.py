from django.shortcuts import render

from django.shortcuts import render
from .models import Student
from rest_framework import generics
from .serializers import StdSerializers

class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        return Student.objects.all()
    
class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Student.objects.all()