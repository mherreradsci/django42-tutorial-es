from django.test import TestCase, override_settings
from .models import User
from .forms import CustomAuthForm

class AutenticationFormTest(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     super(AutenticationFormTest, cls).setUpClass()
    #     cls.u1 = User.objects.create_user(
    #         username="inactive", password="passwordXrtfn123", email="testclient@example.com", is_active=False
    #     )

    @classmethod
    def setUpTestData(cls):

        cls.u1 = User.objects.create_user(
            username="inactive", password="passwordXrtfn123", email="testclient@example.com", is_active=False
        )

        cls.u2 = User.objects.create_user(
            username="badbunny", password="som37560", email="badbunny@example.com"
        )

        # Use an authentication backend that rejects inactive users.
    @override_settings(
        AUTHENTICATION_BACKENDS=[
            "django.contrib.auth.backends.AllowAllUsersModelBackend"]
    )
    def test_inactive_user(self):

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
