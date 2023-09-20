from django import forms
from django.forms.models import inlineformset_factory

from devices.models import Device
from mac_addresses.forms import MacAddressForm
from mac_addresses.models import MacAddress

DeviceMacAddressFormset = inlineformset_factory(
    Device,
    MacAddress,
    form=MacAddressForm,
    extra=0,
    can_delete=True,
    can_delete_extra=True,
)


class DeviceForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields["active"].disabled = True
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["active"].initial = instance.active

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
                attrs={
                    "class": "datetimefield",
                    "placeholder": "YYYY-MM-DD HH24:MI:SS",
                },
            ),
            "active_until": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={
                    "class": "datetimefield",
                    "placeholder": "YYYY-MM-DD HH24:MI:SS",
                },
            ),
        }
