from django.contrib import admin

from .models import Message, Attachment

admin.site.register([Message, Attachment])