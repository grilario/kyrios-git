import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.core.files.storage import default_storage

from io import BytesIO
from PIL import Image

from utils.generators import generateNameFile


class Account(AbstractUser):
    picture = models.ImageField(blank=True, upload_to=generateNameFile)
    biography = models.CharField(max_length=300, blank=True)

    # convert image to jpeg
    def save(self, *args, **kwargs):
        if self.picture and not default_storage.exists(self.picture.path):
            filename = os.path.splitext(self.picture.name)[0] + '.jpg'

            image = Image.open(self.picture)
            imageTmp = BytesIO()
            image.save(imageTmp, format='JPEG', quality=100)

            self.picture.save(filename, ContentFile(
                imageTmp.getvalue()), save=False)
        super(Account, self).save(*args, **kwargs)


@receiver(models.signals.post_delete, sender=Account)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            path = os.path.splitext(instance.picture.path)[0]

            os.remove(path + '.jpg')
            os.remove(path + '_40x.jpg')
            os.remove(path + '_250x.jpg')


@receiver(models.signals.pre_save, sender=Account)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_picture = Account.objects.get(pk=instance.pk).picture
    except Account.DoesNotExist:
        return False

    if not old_picture:
        return False

    new_picture = instance.picture

    if not old_picture == new_picture:
        if os.path.isfile(old_picture.path):
            path = os.path.splitext(old_picture.path)[0]

            os.remove(path + '.jpg')
            os.remove(path + '_40x.jpg')
            os.remove(path + '_250x.jpg')


@receiver(models.signals.post_save, sender=Account)
def auto_generate_different_images_sizes(sender, instance, **kwargs):
    if not instance.picture:
        return False

    filename = os.path.splitext(instance.picture.path)[0]

    if default_storage.exists(filename + '_40x.jpg'):
        return False

    image = Image.open(instance.picture)

    height = image.height
    width = image.width

    if height == width:
        box = (0, 0, width, height)
    elif width > height:
        point1 = (width / 2) - (height / 2)
        point2 = (width / 2) + (height / 2)
        box = (point1, 0, point2, height)
    else:
        point1 = (height / 2) - (width / 2)
        point2 = (height / 2) + (width / 2)
        box = (0, point1, width, point2)

    imageTmp = BytesIO()
    img40x40 = image.resize((40, 40), box=box)
    img40x40.save(imageTmp, format='JPEG', quality=100)
    default_storage.save(filename + '_40x.jpg', imageTmp)

    imageTmp = BytesIO()
    img250x250 = image.resize((250, 250), box=box)
    img250x250.save(imageTmp, format='JPEG', quality=100)
    default_storage.save(filename + '_250x.jpg', imageTmp)
