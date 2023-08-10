from django.test import TestCase

from mac_address_types.forms import MacAddressTypeForm


class DeviceTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"code": "NEW", "name": "NEW Name"}

        form = MacAddressTypeForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
