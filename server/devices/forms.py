from . import models
from django import forms
from django.db import models as django_models


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
