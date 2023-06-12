from django import forms
from .models import MacAddressType

from django.conf import settings

# User = settings.AUTH_USER_MODEL
from django.contrib.admin.widgets import AdminDateWidget


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
            "active_from": AdminDateWidget(attrs={"type": "date"}),
            "active_until": AdminDateWidget(attrs={"type": "date"}),
        }
