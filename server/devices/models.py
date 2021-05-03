from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.html import format_html


# Create your models here.
class Device(models.Model):
    id = models.fields.CharField(max_length=512, unique=True, primary_key=True)
    name = models.CharField(help_text='Custom name for device', max_length=64, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Device(id="{self.id}")'

    # todo: add count of people inside


def picture_path(instance, filename):
    base_dir = f'faces/{instance.user}' if isinstance(
        instance, Face) else f'log/{instance.device}/{instance.face}/{instance}'
    filename = f"{instance.face_id}-{filename.strip().replace(' ', '_')}" if isinstance(
        instance, Face) else f'{instance.time}.{filename.split(".")[-1]}'
    return f'{base_dir}/{filename}'


class Face(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=False, null=False)
    face_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, blank=True, help_text='Custom name for surveilled face')
    image = models.ImageField(upload_to=picture_path, blank=False)
    embedding = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'face_id',)

    def picture(self):
        res = f'<img src="{self.image.url}" width="50vw">'
        return format_html(res)

    def __str__(self):
        return f'Face(name="{self.name}")'


class Log(models.Model):
    face = models.ForeignKey(to=Face, blank=False, null=False, on_delete=models.CASCADE)
    device = models.ForeignKey(to=Device, blank=False, null=False, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to=picture_path)
    # kind
    ENTRY = 'E'
    EXIT = 'L'
    kind_choices = [
        (ENTRY, 'Entered'),
        (EXIT, 'Left')
    ]
    kind = models.CharField(max_length=1, null=False, blank=False, choices=kind_choices)
