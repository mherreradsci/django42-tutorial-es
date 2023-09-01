from django.conf.locale.en import formats as en_formats
from django.contrib import admin

from common import models_utilities
from customers.models import Customer
from devices.models import DeviCustAssignment

en_formats.DATETIME_FORMAT = "d-m-Y H:i:s"


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
    readonly_fields = ("created_by", "created_at", "updated_by", "updated_at")


class CustomerAdmin(admin.ModelAdmin):
    inlines = [DeviCustAssignmentInline]
    fields = [
        "id",
        "code",
        "name",
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
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    ]
    readonly_fields = ["id", "created_by", "created_at", "updated_by", "updated_at"]
    search_fields = ["code", "name"]
    ordering = ["name", "-id"]

    def save_model(self, request, obj, form, change):
        models_utilities.save_model(self, request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        models_utilities.save_formset(self, request, form, formset, change)


admin.site.register(Customer, CustomerAdmin)
