from . import views
from django.urls import path
from django.shortcuts import redirect

urlpatterns = [
    path('logon/', views.signup),
    path('', lambda req: redirect('/admin/')),
    path('hello/', views.hello),
    path('introduce/', views.introduce),
    path('fetch/', views.fetch),
    path('log/', views.log)
]
