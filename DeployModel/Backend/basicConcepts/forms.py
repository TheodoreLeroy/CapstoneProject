from django import forms
from .models import *

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'semester']

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ['class_id', 'subject', 'time_start', 'time_end']