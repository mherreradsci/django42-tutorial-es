from django.test import TestCase

from django.contrib.auth import get_user_model
from django.http import HttpRequest

# from accounts.models import User
from .models import Customer
from .forms import CustomerForm


class CustomerTestCase(TestCase):
    # @classmethod
    # def setUpTestData(cls):
    #     User = get_user_model()
    #     cls.u1 = User.objects.create_user(
    #         username="testuser", password="password", email="testuser@example.com", is_active=False
    #     )

    def test_form_fileds_disabled(self):
        form_data = {"code": "CUS001", "name": "Customer 001"}

        form = CustomerForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
