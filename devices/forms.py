from django import forms
from .models import Device

from mac_addresses.models import MacAddress
from django.forms.models import inlineformset_factory


MacAddressFormset = inlineformset_factory(
    Device,
    MacAddress,
    fields=[
        "address",
        "maad_type",
    ],
    extra=0,
    can_delete=True,
)


class DeviceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = Device

        fields = [
            "id",
            "code",
            "name",
            "ipv4",
            "ipv6",
            "active",
            "active_from",
            "active_until",
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
            "active_from": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
            "active_until": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
        }
