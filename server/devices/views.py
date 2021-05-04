from django.contrib.auth import login, authenticate
from . import forms
from . import utils
from . import models
from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../admin/')
    else:
        form = forms.UserCreationForm()
    return render(request, 'admin/logon.html', {'form': form, 'site_header': admin.site.site_header})


@method_decorator(csrf_exempt, name='dispatch')
def hello(request) -> JsonResponse:
    """hello API endpoint, clients request for access tokens through this api by their device_id"""
    data = json.loads(request.body)
    try:
        device_id = data['device_id']
        if (device := models.Device.objects.filter(id=device_id)).count():
            device = device[0]
        else:
            # registering newly connected device (waiting for user to claim)
            device = models.Device(id=data['device_id'])
            device.save()
        if not device.user:
            return JsonResponse(data=utils.base_response(ok=False, description='Device is yet to be claimed by a user'))
        tokens = models.AccessToken.objects.filter(device=device)
        if tokens.count():
            # request for new token -> invalidate old token
            last_token = tokens.latest('time')
            last_token.valid = False
            last_token.save()
        # create new access token
        token = models.AccessToken(device=device, ip=utils.get_client_ip(request))
        token.save()
        return JsonResponse(data=utils.base_response(response=dict(token=token.token)))
    except KeyError:
        return JsonResponse(data=utils.base_response(ok=False, description='No `device_id` specified'))
