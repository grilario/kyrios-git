import os

from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.dispatch import receiver
from django.core.files.storage import default_storage

from io import BytesIO
from PIL import Image

from utils.generators import generateID, generateNameFile

UserModel = get_user_model()


class Community(models.Model):
    id = models.CharField(primary_key=True, default=generateID, max_length=12)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    picture = models.ImageField(blank=True, upload_to=generateNameFile)
    members = models.ManyToManyField(UserModel, through='Member', through_fields=('community', 'account'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def pictureName(self):
        return os.path.splitext(self.picture.name)[0]
    
    def save(self, *args, **kwargs):
      if self.picture and not default_storage.exists(self.picture.path):
          filename = os.path.splitext(self.picture.name)[0] + '.jpg'

          image = Image.open(self.picture)
          imageTmp = BytesIO()
          image.save(imageTmp, format='JPEG', quality=100)

          self.picture.save(filename, ContentFile(
              imageTmp.getvalue()), save=False)
      super(Community, self).save(*args, **kwargs)


class Member(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    account = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    isOrganizer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(models.signals.post_delete, sender=Community)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            path = os.path.splitext(instance.picture.path)[0]

            os.remove(path + '.jpg')
            os.remove(path + '_70x.jpg')
            os.remove(path + '_130x.jpg')
            os.remove(path + '_210x.jpg')


@receiver(models.signals.pre_save, sender=Community)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_picture = Community.objects.get(pk=instance.pk).picture
    except Community.DoesNotExist:
        return False

    if not old_picture:
        return False

    new_picture = instance.picture

    if not old_picture == new_picture:
        if os.path.isfile(old_picture.path):
            path = os.path.splitext(old_picture.path)[0]

            os.remove(path + '.jpg')
            os.remove(path + '_70x.jpg')
            os.remove(path + '_130x.jpg')
            os.remove(path + '_210x.jpg')


@receiver(models.signals.post_save, sender=Community)
def auto_generate_different_images_sizes(sender, instance, **kwargs):
    if not instance.picture:
        return False

    filename = os.path.splitext(instance.picture.path)[0]

    if default_storage.exists(filename + '_70x.jpg'):
        return False

    image = Image.open(instance.picture)

    height = image.height
    width = image.width

    point1 = (height / 2) - (width * 4 / 21 / 2)
    
    if width == height or point1 > 0:
        point2 = (height / 2) + (width * 4 / 21 / 2)
        box = (0, point1, width, point2)
    else:
        point1 = (width / 2) - (height * 21 / 4 / 2)
        point2 = (width / 2) + (height * 21 / 4 / 2)
        box = (point1, 0, point2, height)

    imageTmp = BytesIO()
    img250x250 = image.resize((360, 70), box=box)
    img250x250.save(imageTmp, format='JPEG', quality=100)
    default_storage.save(filename + '_70x.jpg', imageTmp)

    imageTmp = BytesIO()
    img250x250 = image.resize((680, 130), box=box)
    img250x250.save(imageTmp, format='JPEG', quality=100)
    default_storage.save(filename + '_130x.jpg', imageTmp)

    imageTmp = BytesIO()
    img40x40 = image.resize((1100, 210), box=box)
    img40x40.save(imageTmp, format='JPEG', quality=100)
    default_storage.save(filename + '_210x.jpg', imageTmp)