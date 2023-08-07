from django.test import TestCase

from .forms import DeviceForm


class DeviceTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"code": "DEV001", "name": "Device 001"}

        form = DeviceForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)
