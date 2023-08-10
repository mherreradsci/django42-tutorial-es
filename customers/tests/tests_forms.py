from django.test import TestCase

from customers.forms import CustomerForm


class CustomerTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"code": "CUS001", "name": "Customer 001"}

        form = CustomerForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
