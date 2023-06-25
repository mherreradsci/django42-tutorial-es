from django import forms
from .models import MacAddressType

from django.conf import settings


class MacAddressTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MacAddressTypeForm, self).__init__(*args, **kwargs)
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = MacAddressType
        # fields = "__all__"

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
            "active_from": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
            "active_until": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
        }
