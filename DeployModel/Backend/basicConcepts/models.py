from django.db import models
from django import forms

# Create your models here.
class User(models.Model):
    UserId = models.IntegerField(primary_key=True, db_column="User ID")
    Email = models.EmailField()
    Password = models.CharField(widget=forms.PasswordInput)
    UserName = models.CharField(max_length=255)    

    def __str__(self) -> str:
        return self.UserId + '  ' + self.UserName + '  ' + self.Email

class Student(models.Model):
    StuId = models.IntegerField(primary_key=True, db_column="Student ID")
    StuName = models.CharField(max_length=255, db_column="Student name")
    StuImg = models.ImageField()

    def __str__(self) -> str:
        return self.StuId + '   ' + self.StuName + '    ' + self.StuImg
    
class Teacher(models.Model):
    TeachId = models.IntegerField(primary_key=True, db_column="Teacher ID")
    TeachName = models.models.CharField(_("Teacher name"), max_length=255)
    
    def __str__(self) -> str:
        return self.TeachId + '     ' + self.TeachName