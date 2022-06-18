import os

from django.db import models
from django.dispatch import receiver

from apps.communities.models import Community

from utils.generators import generateID, renameFileWithUUID

class Message(models.Model):
  id = models.CharField(primary_key=True, default=generateID, max_length=12)
  title = models.CharField(max_length=100)
  content = models.CharField(max_length=500)
  community = models.ForeignKey(Community, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Attachment(models.Model):
    task = models.ForeignKey(Message, on_delete=models.CASCADE)
    file = models.FileField(upload_to=renameFileWithUUID)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        uuid, filename = self.file.name.split('_', 1)

        return uuid + '/' + filename

@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)