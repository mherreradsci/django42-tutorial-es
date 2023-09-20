from django.contrib import admin

from common import models_utilities

from .models import MacAddress


class MacAddressAdmin(admin.ModelAdmin):
    fields = [
        "id",
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

    list_display = [
        "id",
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
        "id",
        "active",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    search_fields = ["address"]
    ordering = ["-id"]
    list_per_page = 15  # No of records per page

    def active(self, obj):
        return obj.active

    active.boolean = True

    def save_model(self, request, obj, form, change):
        models_utilities.save_model(self, request, obj, form, change)


admin.site.register(MacAddress, MacAddressAdmin)
