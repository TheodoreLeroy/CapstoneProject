from django.db import models
from django import forms

# Create your models here.

class Student(models.Model):
    StuId = models.IntegerField(primary_key=True, db_column="Student ID")
    StuName = models.CharField(max_length=50, db_column="Student name")
    StuImg = models.ImageField()

    def __str__(self) -> str:
        return self.StuId + '   ' + self.StuName + '    ' + self.StuImg
    
class Teacher(models.Model):
    TeachId = models.IntegerField(primary_key=True, db_column="Teacher ID")
    TeachName = models.CharField(("Teacher name"), max_length=50)
    Email = models.EmailField()
    Pass = models.CharField(forms.PasswordInput, max_length=50)

    def __str__(self) -> str:
        return self.TeachId + '     ' + self.TeachName
    
class Class(models.Model):
    ClassId = models.IntegerField(primary_key=True)
    Semester = models.CharField(max_length=50)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()

    def __str__(self) -> str:
        return super().__str__()
    

class Slot(models.Model):
    SlotId = models.IntegerField(primary_key=True)
    SlotTime = models.DateField(auto_now=True)
    SlotSubject = models.CharField(max_length=50)
    def __str__(self) -> str:
        return super().__str__()
    

    
class TimeFrame(models.Model):
    Id = models.IntegerField(primary_key=True)
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    Time = models.DateTimeField()
    image = models.ImageField()

    def __str__(self) -> str:
        return super().__str__()
    
class AttendanceManager(models.Model):
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    ClassId = models.ForeignKey(Class, on_delete=models.CASCADE)
    TimeFrameId = models.ForeignKey(TimeFrame, on_delete=models.CASCADE)
    Attend = models.BinaryField()

    def __str__(self) -> str:
        return super().__str__()
    
class Log(models.Model):
    SlotId = models.ForeignKey(Slot, on_delete=models.CASCADE)
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    TimeFrameId = models.ForeignKey(TimeFrame, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return super().__str__()