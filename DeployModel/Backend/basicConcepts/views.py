from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from rest_framework import generics
from .models import *
from .serializers import *

class InitialForm(View):
    # def my_custom_sql_view(self, request):
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM ")
    def get(self, request):
        return HttpResponse('<h1>Xin chao</h1>')
    
from .forms import ClassForm
class AddClass(View):
    def add_class(request):
        if request.method == 'POST':
            form = ClassForm(request.POST)
            if form.is_valid():
                
                form.save()
                return redirect('class-list')  # Replace with the name of your list view URL
        else:
            form = ClassForm()
        return render(request, 'add_class.html', {'form': form})

from django.views.generic import ListView
from .models import Class

class ClassListView(ListView):
    model = Class
    template_name = 'class_list.html'  # Specify your template name
    context_object_name = 'classes'

class ClassListCreate(generics.ListCreateAPIView):
    serializer_class = ClassSerializer

    def get_queryset(self):

        return Class.objects.all()

    def perform_create(self, serializer):
        print("asdfgh")
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

class StudentList(generics.ListCreateAPIView):
    serializer_class = StdSerializers

    def get_queryset(self):
        return Student.objects.all()
    
class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = SlotInfomationSerializers

    def get_queryset(self):
        return Slot.objects.all()