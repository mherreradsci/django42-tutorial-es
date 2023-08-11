from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError

from django.utils.translation import gettext as _

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthForm, self).__init__(*args, **kwargs)
        self.error_messages["no_bad_users"] = _(
            "Sorry, accounts starting with 'bad' are not welcome here."
        )

    username = forms.CharField(
        widget=TextInput(attrs={"class": "validate", "placeholder": "Username"})
    )
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

        if user.get_username().startswith("bad"):
            raise ValidationError(
                self.error_messages["no_bad_users"],
                code="no_bad_users",
                # _("Sorry, accounts starting with 'bad' are not welcome here."),
                # code="no_bad_users",
            )


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)  # type: ignore
        error_messages = {
            "username": {
                "unique": _("This account already exist. Please, try another"),
            },
        }
