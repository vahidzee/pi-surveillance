from django.contrib.auth import login, authenticate
from . import forms
from django.shortcuts import render, redirect
from django.contrib import admin


def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../admin/')
    else:
        form = forms.UserCreationForm()
    return render(request, 'admin/logon.html', {'form': form, 'site_header': admin.site.site_header})
