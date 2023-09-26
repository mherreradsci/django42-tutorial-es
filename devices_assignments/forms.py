from django import forms
from django.forms.models import inlineformset_factory

from customers.models import Customer
from devices.models import DeviCustAssignment


class CustomerForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields["active"].disabled = True

        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["active"].initial = instance.active

    class Meta:
        model = Customer
        fields = [
            "code",
            "name",
            "active",
        ]
        widgets = {
            "code": forms.TextInput(attrs={"readonly": "readonly"}),
            "name": forms.TextInput(attrs={"readonly": "readonly"}),
        }


class DeviCustAssignmentForm(forms.ModelForm):
    active = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(DeviCustAssignmentForm, self).__init__(*args, **kwargs)
        self.fields["active"].disabled = True
        self.fields["created_by"].disabled = True
        self.fields["updated_by"].disabled = True

        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.fields["active"].initial = instance.active

    class Meta:
        model = DeviCustAssignment
        fields = [
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
