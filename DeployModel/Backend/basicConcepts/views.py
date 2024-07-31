from rest_framework import generics

from .models import *
from .serializers import *


# CLASS
# get list class - url: "class/"
# create new class- url: "addClass/"
class ClassListCreate(generics.ListCreateAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):

        return Class.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

# get list class that have id - url: "classes/detail/"
class ClassListDetail(generics.ListCreateAPIView):
    serializer_class = ClassDetailSerializer

    def get_queryset(self):

        return Class.objects.all()

# get 1 class with id of that class - url: 
class ClasstDetail(generics.ListCreateAPIView):
    serializer_class = ClassDetailSerializer

    def get_queryset(self):
        class_id = self.kwargs.get('classId')
        return Class.objects.filter(id = class_id)
            
# get list class - urls: "class/delete" - not done
# class ClassDelete(generics.DestroyAPIView):
#     serializer_class = ClassSerializer

#     def delete_queryset(self):
#         id = self.request.id
#         return Class.objects.filter(id=id)


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
        return Student.objects.filter(class_id = id)

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
        return Slot.objects.filter(class_id = id)
    
# Get 1 slot-information with id - url: "slot<int:slotId>/"
class SlotInfomationFromId(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        id = self.kwargs.get('slotId')
        return Slot.objects.filter(id = id)



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