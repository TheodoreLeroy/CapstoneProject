from django.shortcuts import render

from django.shortcuts import render
from .models import Student, Slot
from rest_framework import generics
from .serializers import StdSerializers, SlotInfomationSerializers

class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        return Student.objects.all()
    
class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()