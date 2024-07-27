from .models import Student, Slot
from rest_framework import serializers


class StdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["StuId", "StuName", "StuImg"]

class SlotInfomationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ["StuId", "StuName", "StuImg"]

    