import json

from PIL import Image
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.html import format_html
from . import utils
from io import BytesIO
from django.core.files.base import ContentFile


# Create your models here.
class Device(models.Model):
    id = models.fields.CharField(max_length=512, unique=True, primary_key=True)
    name = models.CharField(help_text='Custom name for device', max_length=64, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Device(id="{self.id}")'

    def inside_count(self) -> int:
        if not (logs := Log.objects.filter(device=self)):
            return 0
        return logs.filter(kind=Log.ENTRY).count() - logs.filter(kind=Log.EXIT).count()

    inside_count.short_description = "Inside Count"
    inside_count.long_description = "How many people entered but did not exit"

    def last_update(self) -> str:
        if not (last_log := Log.objects.filter(device=self)):
            return '-'
        return utils.time_passed(last_log.latest('time').time)

    last_update.short_description = "Last Log"
    last_update.long_description = "Time of last log"


class AccessToken(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    device = models.ForeignKey(to=Device, null=False, blank=False, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(blank=False, null=False)
    valid = models.BooleanField(blank=False, null=False, default=True)


def picture_path(instance, filename):
    base_dir = f'faces/{instance.user}' if isinstance(
        instance, Face) else f'logs/{instance.device.id}/{instance.face.id}'
    filename = f"{instance.id}-{filename.strip().replace(' ', '_')}" if isinstance(
        instance, Face) else f'{instance.time}.{filename.split(".")[-1]}'
    return f'{base_dir}/{filename}'


class Face(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=80, blank=True, help_text='Custom name for surveilled face', null=True)
    image = models.ImageField(upload_to=picture_path, blank=False)
    embedding = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'id',)

    def picture(self):
        res = f'<img src="{self.image.url}" width="50vw">'
        return format_html(res)

    def last_seen(self):
        if not (last_log := Log.objects.filter(face=self)):
            return '-'
        last_log = last_log.latest('time')
        return f'{dict(Log.kind_choices)[last_log.kind]} {last_log.device_name()} {utils.time_passed(last_log.time)}'

    def __str__(self):
        return f'Face(name="{self.name if self.name else self.id}")'

    @staticmethod
    def save_pil(user, image: Image, embedding=None, name=None):
        print(user, image)
        if embedding is not None and hasattr(embedding, 'tolist'):
            embedding = json.dumps(embedding.tolist())
        instance = Face(user=user, embedding=embedding, name=name)
        stream = BytesIO()
        try:
            image.save(stream, format='png')
            instance.image.save(instance.image.name, ContentFile(stream.getvalue()))
        finally:
            stream.close()
        instance.save()


class Log(models.Model):
    face = models.ForeignKey(to=Face, blank=False, null=False, on_delete=models.CASCADE)
    device = models.ForeignKey(to=Device, blank=False, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=picture_path, null=True, blank=True)
    # kind
    ENTRY = 'E'
    EXIT = 'L'
    kind_choices = [
        (ENTRY, 'Entered'),
        (EXIT, 'Left')
    ]
    kind = models.CharField(max_length=1, null=False, blank=False, choices=kind_choices)

    def __str__(self):
        return f'Log(face="{self.face}", device="{self.device}", kind="{self.kind}", time="{self.time}")'

    def device_name(self) -> str:
        return self.device.name if self.device.name else self.device.id

    device_name.short_description = "Device"

    def face_name(self) -> str:
        return self.face.name if self.face.name else self.face.id

    face_name.short_description = "Face"

    def picture(self):
        if self.image:
            res = f'<img src="{self.image.url}" width="50vw">'
            return format_html(res)
        return self.face.picture()
