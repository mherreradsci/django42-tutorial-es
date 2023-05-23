from django import forms
from .models import Device

from django.conf import settings

User = settings.AUTH_USER_MODEL


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = Device
        # fields = "__all__"

        fields = [
            "id",
            "code",
            "name",
            "ipv4",
            "ipv6",
            "active",
            "created_by",
            "updated_by",
        ]

        widgets = {
            "code": forms.TextInput(
                attrs={
                    "placeholder": "code",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "placeholder": "name",
                }
            ),
            "ipv4": forms.TextInput(
                attrs={
                    "placeholder": "nnn.nnn.nnn.nnn",
                }
            ),
            "ipv6": forms.TextInput(
                attrs={
                    "placeholder": "IP V6 format",
                }
            ),
        }
