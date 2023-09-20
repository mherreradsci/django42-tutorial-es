from django import forms
from django.conf import settings

from mac_address_types.models import MacAddressType


class MacAddressTypeForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(MacAddressTypeForm, self).__init__(*args, **kwargs)
        self.fields["active"].disabled = True
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["active"].initial = instance.active

    class Meta:
        model = MacAddressType

        fields = [
            "id",
            "code",
            "name",
            "desc",
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
            "desc": forms.Textarea(
                attrs={"placeholder": "Description", "rows": settings.TA_DEFAULT_ROWS},
            ),
            # "active": forms.CheckboxInput(),
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
