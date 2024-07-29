from .models import Student, Slot
from rest_framework import serializers

# class LogInSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [""]

class StdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["StuId", "StuName", "StuImg"]

class SlotInfomationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["SlotId", "SlotTime", "SlotSubject"]

    