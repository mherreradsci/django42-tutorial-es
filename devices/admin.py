from django.contrib import admin
from .models import Device
from common.models import AuditInfo
from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "d-m-Y H:i:s"


class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "active",
        "ipv4",
        "ipv6",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]

    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")
    search_fields = ["code", "name"]
    ordering = ["name", "-id"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        elif change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(Device, DeviceAdmin)
