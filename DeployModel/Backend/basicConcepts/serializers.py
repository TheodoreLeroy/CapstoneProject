from .models import *
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
        model = Student
        fields = '__all__'

class SlotInfomationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['class_name', 'semester'] 

    