from django import forms
from django.forms.models import inlineformset_factory

from customers.models import Customer
from devices.models import DeviCustAssignment


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "code",
            "name",
            # "active",
        ]
        widgets = {
            "code": forms.TextInput(attrs={"readonly": "readonly"}),
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
            # "active": forms.CheckboxInput(attrs={"readonly": "readonly", "disabled": True}),
        }


class DeviCustAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeviCustAssignmentForm, self).__init__(*args, **kwargs)
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

    class Meta:
        model = DeviCustAssignment
        fields = [
            # "id",
            # "customer",
            "device",
            "active",
            "active_from",
            "active_until",
            "created_by",
            "updated_by",
            "closing_reason_type",
            "closing_remarks",
        ]
        widgets = {
            "active_from": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "from date/time"},
            ),
            "active_until": forms.DateTimeInput(
                format="%Y-%m-%d %H:%M:%S",
                attrs={"class": "datetimefield", "placeholder": "until date/time"},
            ),
            "closing_remarks": forms.Textarea(attrs={"rows": 1, "cols": 20}),
        }


DeviCustAssignmentFormset = inlineformset_factory(
    Customer,
    DeviCustAssignment,
    form=DeviCustAssignmentForm,
    extra=0,
    can_delete=True,
    can_delete_extra=True,
    min_num=0,
    validate_min=True,
)
