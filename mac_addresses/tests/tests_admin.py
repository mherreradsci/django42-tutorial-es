import copy
from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from accounts.models import User
from devices.models import Device
from mac_address_types.models import MacAddressType
from mac_addresses.admin import MacAddressAdmin
from mac_addresses.models import MacAddress

trace_on = False


def trace(mac_address):
    if trace_on:
        print(
            f"[{str(mac_address.id).ljust(5)}]"
            + f" [{str(mac_address.address).ljust(17)}]"
            + f" [{str(mac_address.maad_type).ljust(15)}]"
            + f" [{str(mac_address.device).ljust(25)}]"
            + f" [{str(mac_address.created_by).ljust(10)}]"
            + f" [{str(mac_address.created_at).ljust(32)}]"
            + f" [{str(mac_address.updated_by).ljust(10)}]"
            + f" [{str(mac_address.updated_at).ljust(32)}]"
        )


class MacAddressAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()
        cls.device = Device(code="ND", name="New Device Name")
        cls.device.save()

    def test_mac_address_admin_save_and_update_model(self):
        if trace_on:
            print(
                f"id".ljust(5 + 3)
                + f"address".ljust(17 + 3)
                + f"maad_type".ljust(15 + 3)
                + f"device".ljust(25 + 3)
                + f"created_by".ljust(10 + 3)
                + f"created_at".ljust(32 + 3)
                + f"updated_by".ljust(10 + 3)
                + f"updated_at".ljust(32 + 3)
            )
        my_model_admin = MacAddressAdmin(model=MacAddress, admin_site=AdminSite())
        self.assertEqual(str(my_model_admin), "mac_addresses.MacAddressAdmin")

        mac_address = MacAddress(
            address="00-00-00-00-00-00",
            maad_type=self.mac_address_type,
            device=self.device,
        )
        trace(mac_address)
        my_model_admin.save_model(
            obj=mac_address, request=Mock(user=self.user), form=None, change=False
        )
        trace(mac_address)
        self.assertTrue(mac_address.created_by, self.user)
        self.assertTrue(mac_address.updated_by, self.user)

        mac_address_copy = copy.deepcopy(mac_address)
        mac_address_copy.address = "00-00-00-00-00-01"
        # trace(mac_address)
        my_model_admin.save_model(
            obj=mac_address_copy, request=Mock(user=self.user), form=None, change=True
        )
        trace(mac_address_copy)

        self.assertLess(mac_address.created_at, mac_address.updated_at)
        self.assertNotEqual(mac_address_copy.address, mac_address.address)

        # mac_address = my_model_admin.get_object(
        #     request=Mock(user=self.user), object_id=str(1)
        # )
        # trace(mac_address)
