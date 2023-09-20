# from django.conf.locale.en import formats as en_formats
from django.contrib import admin

from common import models_utilities
from devices.models import Device, DeviCustAssignment
from mac_addresses.models import MacAddress

# en_formats.DATETIME_FORMAT = "d-m-Y H:i:s"


class MacAddessInline(admin.TabularInline):
    model = MacAddress
    extra = 0
    fields = [
        "address",
        "maad_type",
        "device",
        "active",
        "active_from",
        "active_until",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    readonly_fields = (
        "active",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )

    def active(self, obj):
        return obj.active

    active.boolean = True


class DeviCustAssignmentInline(admin.TabularInline):
    model = DeviCustAssignment
    extra = 0
    fields = [
        "customer",
        "device",
        "active",
        "active_from",
        "active_until",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    readonly_fields = (
        "active",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )

    def active(self, obj):
        return obj.active

    active.boolean = True


class DeviCustAssignmentAdmin(admin.ModelAdmin):
    inlines = [DeviCustAssignmentInline]


class DeviceAdmin(admin.ModelAdmin):
    inlines = [MacAddessInline, DeviCustAssignmentInline]
    fields = [
        "id",
        "code",
        "name",
        "active",
        "active_from",
        "active_until",
        "uuid",
        "ipv4",
        "ipv6",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]

    list_display = [
        "id",
        "code",
        "name",
        "active",
        "active_from",
        "active_until",
        "uuid",
        "ipv4",
        "ipv6",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]

    readonly_fields = (
        "id",
        "uuid",
        "active",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    search_fields = ["code", "name"]
    ordering = [
        "-id",
    ]
    list_per_page = 15  # No of records per page

    def active(self, obj):
        return obj.active

    active.boolean = True

    def save_model(self, request, obj, form, change):
        models_utilities.save_model(self, request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        models_utilities.save_formset(self, request, form, formset, change)


admin.site.register(Device, DeviceAdmin)
