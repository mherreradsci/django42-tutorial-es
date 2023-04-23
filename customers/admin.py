from django.contrib import admin

# Register your models here.
from .models import Customer

from django.conf.locale.en import formats as en_formats

en_formats.DATETIME_FORMAT = "d-m-Y H:i:s"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ["id", "code", "name", "created_at", "updated_at"]
    readonly_fields = ["created_at", "updated_at"]
    search_fields = ["code", "name"]
    ordering = ["name", "-id"]


admin.site.register(Customer, CustomerAdmin)
