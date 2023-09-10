from django.test import TestCase, override_settings

from accounts.forms import CustomAuthForm
from accounts.models import User


class AutenticationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            username="inactive",
            password="passwordXrtfn123",
            email="testclient@example.com",
            is_active=False,
        )

        cls.u2 = User.objects.create_user(
            username="badbunny", password="som37560", email="badbunny@example.com"
        )

        cls.u3 = User.objects.create_user(
            username="someone", password="topsecret", email="someone@example.com"
        )

    # Use the ModelBackend to test invalid_login
    @override_settings(
        AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]
    )
    def test_inactive_user_model_backend(self):
        data = {
            "username": "inactive",
            "password": "passwordXrtfn123",
        }
        form = CustomAuthForm(None, data)

        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.non_field_errors(),
            [
                str(
                    form.error_messages["invalid_login"]
                    % {"username": User._meta.get_field("username").verbose_name}
                )
            ],
        )

    # Use an authentication backend that rejects inactive users.
    @override_settings(
        AUTHENTICATION_BACKENDS=[
            "django.contrib.auth.backends.AllowAllUsersModelBackend"
        ]
    )
    def test_inactive_user_model_allow(self):
        data = {
            "username": "inactive",
            "password": "passwordXrtfn123",
        }
        form = CustomAuthForm(None, data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(), [str(form.error_messages["inactive"])]
        )

    def test_user_startwith_bad(self):
        data = {
            "username": "badbunny",
            "password": "som37560",
        }

        form = CustomAuthForm(None, data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.non_field_errors(), [str(form.error_messages["no_bad_users"])]
        )

    def test_user_ok(self):
        data = {
            "username": "someone",
            "password": "topsecret",
        }

        form = CustomAuthForm(None, data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.non_field_errors(), [])
