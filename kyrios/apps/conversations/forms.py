from django.forms.models import ModelForm
from django import forms

from .models import Message

class MessageForm(ModelForm):
  class Meta:
    model = Message
    fields = ['title', 'description']