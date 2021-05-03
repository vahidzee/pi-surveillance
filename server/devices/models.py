from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Device(models.Model):
    id = models.fields.CharField(max_length=512, unique=True, primary_key=True)
    name = models.CharField(help_text='Custom name for device', max_length=64, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)

    # todo: add count of people inside
