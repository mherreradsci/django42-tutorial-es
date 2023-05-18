from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError

from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code="inactive",
            )
        if user.get_username().startswith("bad"):
            raise ValidationError(
                _("Sorry, accounts starting with 'bad' aren't welcome here."),
                code="no_b_users",
            )

    username = forms.CharField(
        widget=TextInput(attrs={"class": "validate", "placeholder": "Username"})
    )
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
        error_messages = {
            "username": {
                "unique": _("This account already exist. Please, try another"),
            },
        }
