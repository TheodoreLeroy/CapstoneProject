from .models import Student
from rest_framework import serializers


class StdSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["StuId", "StuName", "StuImg"]

    