from PIL import Image
from django.contrib.auth import login, authenticate
from . import forms, recognition
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
    return render(request, 'admin/logon.html',
                  {'form': form, 'site_header': admin.site.site_header, 'site_title': admin.site.site_title})


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
            return JsonResponse(data=utils.base_response(ok=False, message='Device is yet to be claimed by a user'))
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
        return JsonResponse(data=utils.base_response(ok=False, message='No `device_id` specified'))


def authenticate_device(funct):
    @method_decorator(csrf_exempt, name='dispatch')
    def view_wrapper(request, *args, **kwargs):
        if request.POST:
            data = dict(request.POST)
            file = request.FILES.get('image', None)
        else:
            data = json.loads(request.body)
            file = None
        try:
            token = data['token']
            if isinstance(token, list):
                token = token[0]
            access_token = models.AccessToken.objects.get(token=token)
            if not access_token.is_valid(request):
                return JsonResponse(data=utils.base_response(message='This token is no longer valid.', ok=False))
            auth_res = dict(user=access_token.device.user, device=access_token.device)
        except KeyError:
            return JsonResponse(data=utils.base_response(message='No `token` was specified.', ok=False))
        except (models.models.ObjectDoesNotExist, Exception):
            return JsonResponse(data=utils.base_response(message='Invalid `token` was specified.', ok=False))
        return funct(request, *args, data=data, file=file, auth_res=auth_res, **kwargs)

    return view_wrapper


@authenticate_device
def fetch(request, data: dict = None, file=None, auth_res=None):
    return JsonResponse(
        data=utils.base_response(
            response=dict(faces=[
                dict(embedding=face.embedding, face_id=face.id) for face in
                models.Face.objects.filter(user=auth_res['user'])
            ])
        )
    )


@authenticate_device
def introduce(request, data: dict = None, file=None, auth_res=None):
    try:
        embedding = data['embedding']
        embedding = json.loads(embedding if not isinstance(embedding, list) else embedding[0])
        image = Image.open(file).convert('RGB')
        face = recognition.find_face(auth_res['user'], image=image, embedding=embedding)
        if isinstance(face, bool):
            face = models.Face.save_pil(user=auth_res['user'], image=image, embedding=embedding)
        return JsonResponse(data=utils.base_response(response=dict(face_id=face.id)))
    except KeyError:
        return JsonResponse(data=utils.base_response(message='Embedding was not mentioned', ok=False))


@authenticate_device
def log(request, data: dict = None, file=None, auth_res=None):
    try:
        face_id = data['face_id'] if not isinstance(data['face_id'], list) else data['face_id'][0]
        face = models.Face.objects.get(id=face_id)
        kind = data['kind'] if not isinstance(data['kind'], list) else data['kind'][0]
        device = auth_res['device']
        image = Image.open(file).convert('RGB') if file is not None else None
        models.Log.save_pil(face=face, device=device, kind=kind, image=image)
        return JsonResponse(data=utils.base_response(ok=True, message='Logged successfully'))
    except KeyError:
        return JsonResponse(
            data=utils.base_response(message='Both `face_id` and `kind` are expected to be specified', ok=False))
    except (models.models.ObjectDoesNotExist,):
        return JsonResponse(data=utils.base_response(message='Invalid `face_id` is specified', ok=False))
