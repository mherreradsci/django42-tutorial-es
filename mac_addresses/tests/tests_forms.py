from django.test import TestCase

from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.forms import MacAddressForm
from mac_addresses.models import MacAddress


class DeviceTestCase(TestCase):
    def test_form_fileds_disabled(self):
        form_data = {"address": "22-22-22-22-22-22"}

        form = MacAddressForm(data=form_data)
        self.assertTrue(form.fields["created_by"].disabled)
        self.assertTrue(form.fields["updated_by"].disabled)

    def test_form_active_initial(self):
        device = Device.objects.create(code="DEV01")
        maad_type = MacAddressType.objects.create(code="MAT01")
        mac_address = MacAddress.objects.create(
            address="22-22-22-22-22-22", maad_type=maad_type, device=device
        )

        # Check active
        self.assertTrue(mac_address.active)

        form_data = {"address": "22-22-22-22-22-22"}
        form = MacAddressForm(data=form_data, instance=mac_address)

        self.assertTrue(form.fields["active"].initial)
        self.assertInHTML(
            '<input type="checkbox" name="active" disabled id="id_active" checked>',
            str(form),
        )

        # Check inactive
        mac_address.active_from = mac_address.active_until
        self.assertFalse(mac_address.active)

        form = MacAddressForm(data=form_data, instance=mac_address)

        self.assertFalse(form.fields["active"].initial)
        self.assertInHTML(
            '<input type="checkbox" name="active" disabled id="id_active">', str(form)
        )
