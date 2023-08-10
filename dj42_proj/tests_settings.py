from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase

"""
Automated Test for dj42_proj project
"""


class ConfigTest(TestCase):
    def test_secrect_key_strength(self):
        """
        Test secret key strength
        """

        try:
            # Validate if is_strong
            validate_password(settings.SECRET_KEY)
        except Exception as e:
            msg = f"Weak Secret Key {e.messages}"
            self.fail(msg)

    # def test_debug_is_off(self):
    #     """
    #     Test DEBUG is off
    #     https://docs.djangoproject.com/en/4.2/topics/testing/overview/#other-test-conditions
    #     Regardless of the value of the DEBUG setting in your configuration
    #     file, all Django tests run with DEBUG=False.
    #     """
    #     # Se obtiene el valor de .env para hacer el test

    #     ENV_DEBUG = os.environ.get("DEBUG") == "1"
    #     self.assertFalse(ENV_DEBUG)
