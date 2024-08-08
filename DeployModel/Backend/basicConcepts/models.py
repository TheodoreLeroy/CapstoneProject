from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
# Create teacher and student group
# teacher_group, created = Group.objects.get_or_create(name='Teacher')
# student_group, created = Group.objects.get_or_create(name='Student')

# Add auth to teacher
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'), 
    )
    user_type = models.CharField(max_length=50, choices = USER_TYPE_CHOICES)


    
class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    semester = models.CharField(max_length=50)
    date_time = models.DateTimeField(default=timezone.now)
    

    
class Camera(models.Model):
    CameraId = models.IntegerField(primary_key=True, default=1, auto_created=True)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

class Slot(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    time_start = models.TimeField()
    time_end = models.TimeField()
    
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    teach_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    
class Student(models.Model):
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    # slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    # student_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=16)
    embedding = models.BinaryField()

# for each frame in 15 frame in camera
# embedding for image of total class (first or last in 15 frame)
class TimeFrame(models.Model):
    embedding = models.BinaryField(default=b'')
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)

# contain all student that model can recognite in one frame. when it have detect face bt can't recognite std_id = null
class AttendentStudentsAtOneFrame(models.Model):
    embedding = models.JSONField()
    student_id = models.CharField(max_length=255)
    time_frame = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, related_name='attendent_students')

# contain last status of slot 
class Log(models.Model):
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    attend_status = models.BinaryField(default=b'')

# contain status one student for each row after slot
class AttendentStudentsAtAllFrame(models.Model):
    log_id = models.ForeignKey(Log, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255)
    total_attendent = models.IntegerField()
