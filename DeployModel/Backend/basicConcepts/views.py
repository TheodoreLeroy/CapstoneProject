from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.db import connection
from . import models
from django import forms
from rest_framework import generics
from . import serializers as se
from django.contrib.auth import authenticate

class InitialForm(View):
    # def my_custom_sql_view(self, request):
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM ")
    def get(self, request):
        return HttpResponse('<h1>Xin chao</h1>')
    
from django.shortcuts import render, redirect
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

class StudentList(generics.ListCreateAPIView):
    serializer_class = se.StdSerializers

    def get_queryset(self):
        return models.Student.objects.all()
    
class SlotInfomation(generics.ListCreateAPIView):
    serializer_class = se.SlotInfomationSerializers

    def get_queryset(self):
        return models.Slot.objects.all()