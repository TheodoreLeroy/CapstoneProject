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

class ClassListDetailCreate(generics.ListCreateAPIView):
    serializer_class = ClassDetailSerializer

    def get_queryset(self):

        return Class.objects.all()
            
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
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

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



# __________________ HA DJANGO ___________________________
            

from django.shortcuts import render, redirect
from .forms import ClassForm

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