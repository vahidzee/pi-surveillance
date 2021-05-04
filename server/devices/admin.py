from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models
from . import forms


# Register your models here.
class FilterUserAdmin(admin.ModelAdmin):
    exclude = ['user']

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
    actions = None
    sortable_by = 'last_update'
    form = forms.DeviceForm
    list_display = ['id', 'name', 'last_update', 'inside_count']
    list_editable = ['name']
    list_display_links = None

    def save_model(self, request, obj, form, change):
        found_obj = models.Device.objects.get(id=obj.id)
        if found_obj.user is not None and found_obj.user != request.user:
            return  # this device has already been registered
        found_obj.user = request.user
        found_obj.name = obj.name
        found_obj.save()


@admin.register(models.Face)
class FaceAdmin(FilterUserAdmin):
    list_display = ['name', 'picture', 'image', 'last_seen']
    list_display_links = None
    list_editable = ['image', 'name']
    list_select_related = True


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ['face_name', 'device_name', 'time', 'kind', 'picture']
    list_display_links = None
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    # Allow viewing objects but not actually changing them.
    def has_change_permission(self, request, obj=None):
        return (request.method in ['GET', 'HEAD'] and
                super().has_change_permission(request, obj))

    def get_queryset(self, request):
        qs = super(LogAdmin, self).get_queryset(request)
        return qs.filter(device__user=request.user)


admin.site.site_header = "Surveillance Manager"
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(models.AccessToken)
