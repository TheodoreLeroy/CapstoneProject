from . import models
from django import forms
from rest_framework import serializers

# class LogInSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [""]

# To create new class
# class ClassForm(serializers.ModelSerializer):
#     class Meta:
#         model = models.Class
#         fields = ['className', 'semester', ]

class StdSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ["StuId", "StuName", "StuImg"]

class SlotInfomationSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Slot
        fields = ["SlotId", "SlotTime", "SlotSubject"]

    