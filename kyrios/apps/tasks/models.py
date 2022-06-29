import os

from django.db import models
from django.dispatch import receiver

from apps.communities.models import Community
from apps.accounts.models import Account

from utils.generators import generateID, renameFileWithUUID


class Task(models.Model):
    id = models.CharField(primary_key=True, default=generateID, max_length=12)
    title = models.CharField('Título', max_length=100)
    description = models.CharField('Descrição', max_length=500)
    delivery_to = models.DateTimeField('Data de entrega')
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to=renameFileWithUUID)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        uuid, filename = self.file.name.split('_', 1)

        return filename

    def link(self):
        uuid, filename = self.file.name.split('_', 1)

        return uuid + '/' + filename
    


@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
