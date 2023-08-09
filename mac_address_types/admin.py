from django.contrib import admin
from .models import MacAddressType


class MacAddressTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "code",
        "name",
        "desc",
        "active",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]

    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")
    search_fields = ["code", "desc"]
    ordering = ["-id"]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        elif change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(MacAddressType, MacAddressTypeAdmin)
