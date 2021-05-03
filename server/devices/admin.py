from django.contrib import admin
from django.contrib.auth.models import User, Group
from . import models


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
            # the changelist itself
            return True
        return obj.user == request.user


@admin.register(models.Device)
class DeviceAdmin(FilterUserAdmin):
    list_display = ['id', 'name']


admin.site.site_header = "Surveillance Manager"
admin.site.unregister(User)
admin.site.unregister(Group)
