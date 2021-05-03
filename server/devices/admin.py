from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models
from . import forms


# Register your models here.
class FilterUserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(FilterUserAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            return True
        return obj.user == request.user


@admin.register(models.Device)
class DeviceAdmin(FilterUserAdmin):
    form = forms.DeviceForm
    list_display = ['id', 'name']

    def save_model(self, request, obj, form, change):
        obj = models.Device.objects.get(id=obj.id)
        obj.user = request.user
        obj.save()


admin.site.site_header = "Surveillance Manager"
admin.site.unregister(User)
admin.site.unregister(Group)
