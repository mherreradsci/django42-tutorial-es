from django import forms

from mac_addresses.models import MacAddress
from mac_addresses.validators import validate_mac_address


class MacAddressForm(forms.ModelForm):
    address = forms.CharField(validators=[validate_mac_address])
    active = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(MacAddressForm, self).__init__(*args, **kwargs)
        self.fields["active"].disabled = True
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["active"].initial = instance.active

    class Meta:
        model = MacAddress

        fields = [
            "address",
            "maad_type",
            "active",
            "active_from",
            "active_until",
            "created_by",
            "updated_by",
        ]

        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "XX-XX-XX-XX-XX-XX",
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
