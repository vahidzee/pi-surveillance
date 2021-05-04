from PIL import Image

from . import models, recognition
from django import forms
from django.db import models as django_models

from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        exclude = ['user']

    def clean(self):
        dev_id = self.cleaned_data.get('id')
        try:
            if models.Device.objects.get(id=dev_id).user is not None:
                pass
                # raise forms.ValidationError("This Device has already been registered")
        except django_models.ObjectDoesNotExist:
            raise forms.ValidationError("Device has not been connected to server yet")
        return self.cleaned_data


class FaceForm(forms.ModelForm):
    class Meta:
        model = models.Face
        exclude = ['user', 'embedding']

    def clean(self):
        dev_id = self.cleaned_data.get('id')
        if not recognition.get_faces(image=Image.open(self.cleaned_data.get('image'))):
            raise forms.ValidationError("No face could be found in the provided image")
        return self.cleaned_data


class UserCreationForm(AuthUserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
