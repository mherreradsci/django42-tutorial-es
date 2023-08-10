from django.test import TestCase

from mac_addresses.forms import MacAddressForm


class DeviceTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"address": "22-22-22-22-22-22"}

        form = MacAddressForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
