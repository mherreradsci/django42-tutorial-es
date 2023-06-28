from django import forms
from .models import MacAddress


class MacAddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MacAddressForm, self).__init__(*args, **kwargs)
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = MacAddress
        # fields = '__all__'
        fields = [
            "address",
            "maad_type",
            "active_from",
            "active_until",
            "created_by",
            "updated_by",
        ]

        widgets = {
            "address": forms.TextInput(
                attrs={
                    "placeholder": "MAC Address",
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
