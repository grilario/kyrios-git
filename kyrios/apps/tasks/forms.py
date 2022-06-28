from django.forms.models import ModelForm
from django import forms

from .models import Task

class TaskForm(ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'delivery_to']
    widgets = {
      'delivery_to': forms.DateTimeInput(attrs={'type': 'datetime-local'})
    }

class FileFieldForm(forms.Form):
  file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))