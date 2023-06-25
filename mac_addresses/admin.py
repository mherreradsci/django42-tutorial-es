from django.contrib import admin
from .models import MacAddress

# from django.conf.locale.en import formats as en_formats

# en_formats.DATETIME_FORMAT = "m-d-Y H:i:s"


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

    readonly_fields = ("id", "created_by", "created_at", "updated_by", "updated_at")
    search_fields = ["address"]
    ordering = ["-id"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        elif change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(MacAddress, MacAddressAdmin)
