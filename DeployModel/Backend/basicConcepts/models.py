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
    ClassName = models.CharField(max_length=50, default="")
    Semester = models.CharField(max_length=50)
    dateTime = models.DateTimeField(default=timezone.now)
    

    def __str__(self) -> str:
        return super().__str__()
    
class Camera(models.Model):
    Id = models.CharField(primary_key=True,max_length=50)
    classId = models.ForeignKey(Class, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

class Slot(models.Model):
    ClassId = models.ForeignKey(Class, on_delete=models.CASCADE)
    SlotId = models.IntegerField(primary_key=True)
    Subject = models.CharField(max_length=50)
    Time_start = models.TimeField()
    Time_end = models.TimeField()
    def __str__(self) -> str:
        return super().__str__()
    
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ClassId = models.ForeignKey(Class, on_delete=models.CASCADE)
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    TeachId = models.IntegerField(primary_key=True, db_column="Teacher ID")
    TeachName = models.CharField(("Teacher name"), max_length=50)
    Email = models.EmailField()
    Pass = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.TeachId + '     ' + self.TeachName
    
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ClassId = models.ForeignKey(Class, on_delete=models.CASCADE)
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    StuId = models.IntegerField(primary_key=True, db_column="Student ID")
    StuName = models.CharField(max_length=50, db_column="Student name")
    Email =models.EmailField()
    Pass = models.CharField(max_length=16)
    StuImg = models.ImageField()

    def __str__(self) -> str:
        return self.StuId + '   ' + self.StuName + '    ' + self.StuImg


class TimeFrame(models.Model):
    ClassId = models.ForeignKey(Class,on_delete=models.CASCADE)
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    Time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()
    
class Log(models.Model):
    ClassId = models.IntegerField()
    SlotId = models.IntegerField()
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    Attend_Status = models.BinaryField(default=0)

    def __str__(self) -> str:
        return super().__str__()