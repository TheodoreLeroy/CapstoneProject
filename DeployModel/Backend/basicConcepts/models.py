from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
import os
from datetime import datetime


# Create your models here.
# Create teacher and student group
# teacher_group, created = Group.objects.get_or_create(name='Teacher')
# student_group, created = Group.objects.get_or_create(name='Student')
from pathlib import Path


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)


class Class(models.Model):
    class_name = models.CharField(max_length=50, unique=True)
    semester = models.CharField(max_length=50)
    date_time = models.DateTimeField(default=timezone.now)


class Camera(models.Model):
    CameraId = models.IntegerField(
        primary_key=True, default=1, auto_created=True)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)


class Slot(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    time_start = models.TimeField()
    time_end = models.TimeField()
    status = models.BooleanField(default=False)


class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    teach_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)


class Student(models.Model):
    def student_image_path(instance, filename):
        # clas_name = Class.objects.filter(id=instance.class_id_id)
        clas_name = instance.class_id.class_name
        # File will be uploaded to MEDIA_ROOT/Data/classes/<class_name>/<student_id>_<student_name>.jpg
        return f'Data/classes/{clas_name}/{instance.student_id}_{instance.name}/{instance.student_id}_{instance.name}.jpg'

    student_id = models.AutoField(primary_key=True)
    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    # slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    # student_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=16)
    image = models.ImageField(upload_to=student_image_path)


# for each frame in 15 frame in camera
# embedding for image of total class (first or last in 15 frame)


class TimeFrame(models.Model):
    def query_class(instance):
        slot_instance = Slot.objects.get(id=instance.id)
        slot_name = slot_instance.subject
        class_instance = Class.objects.get(id=slot_instance.class_id.id)
        clas_name = class_instance.class_name
        return clas_name, slot_name

    def student_image_path(instance, filename):

        clas_name, slot_name = TimeFrame.query_class(instance.slot_id)
        current_datetime = datetime.now().strftime('%Y%m%d%H%M')
        if instance.id is None:

            # Return a temporary path if the instance is not saved yet
            return f'Data/classes/temp/{filename}'
        # File will be uploaded to MEDIA_ROOT/Data/classes/<class_name>/<student_id>_<student_name>.jpg
        return f'Data/classes/{clas_name}/slot/{slot_name}/images/{instance.id}_{current_datetime}.jpg'

    embedding = models.ImageField(upload_to=student_image_path)
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)


# contain all student that model can recognite in one frame. when it have detect face bt can't recognite std_id = null


class AttendentStudentsAtOneFrame(models.Model):
    embedding = models.JSONField()
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    time_frame = models.ForeignKey(
        TimeFrame, on_delete=models.CASCADE, related_name='time_frame')

# contain last status of slot


class Log(models.Model):
    slot_id = models.ForeignKey(Slot, on_delete=models.CASCADE)
    attend_status = models.BinaryField(default=b'')

# contain status one student for each row after slot


class AttendentStudentsAtAllFrame(models.Model):
    log_id = models.ForeignKey(Log, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255)
    total_attendent = models.IntegerField()
