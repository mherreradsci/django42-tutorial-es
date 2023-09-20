from django.contrib import admin

from common import models_utilities
from mac_address_types.models import MacAddressType


class MacAddressTypeAdmin(admin.ModelAdmin):
    fields = [
        "code",
        "name",
        "desc",
        "active",
        "active_from",
        "active_until",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    list_display = [
        "id",
        "code",
        "name",
        "desc",
        "active",
        "active_from",
        "active_until",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]

    readonly_fields = ("active", "created_by", "created_at", "updated_by", "updated_at")
    search_fields = ["code", "desc"]
    ordering = ["-id"]
    list_per_page = 15  # No of records per page

    def active(self, obj):
        return obj.active

    active.boolean = True

    def save_model(self, request, obj, form, change):
        models_utilities.save_model(self, request, obj, form, change)


admin.site.register(MacAddressType, MacAddressTypeAdmin)
