from .models import *
from rest_framework import serializers


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


class ClassDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class CameraInfor(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class TimeFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeFrame
        fields = '__all__'


class AttendentStudentsAtOneFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendentStudentsAtOneFrame
        fields = ['slot', 'student_id', 'time_frame']


class LogDetail(serializers.ModelSerializer):
    class Meta:
        model = Logs
        fields = '__all__'


class CamInfo(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'

# class LogInSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [""]

# To create new class
# class ClassForm(serializers.ModelSerializer):
#     class Meta:
#         model = models.Class
#         fields = ['className', 'semester', ]
