from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    active_from = forms.DateTimeInput()
    active_until = forms.DateTimeInput()

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        # self.fields['active_from'].widget = widgets.AdminDateWidget(attrs={"type": "date"})
        # self.fields['active_from_time'].widget = widgets.AdminTimeWidget(attrs={"type": "time"})
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = Customer

        fields = [
            "id",
            "code",
            "name",
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
            "active_from": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
            "active_until": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until"},
            ),
        }
