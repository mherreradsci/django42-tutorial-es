from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = Customer

        # specify fields to be used
        fields = [
            "id",
            "code",
            "name",
            # "created_at",
        ]
