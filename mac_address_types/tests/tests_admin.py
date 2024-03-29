import copy
import time
from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from accounts.models import User
from mac_address_types.admin import MacAddressTypeAdmin
from mac_address_types.models import MacAddressType

trace_on = False


def trace(mac_address_type):
    if trace_on:
        print(
            f"[{str(mac_address_type.id).ljust(5)}]"
            + f" [{mac_address_type.name.ljust(30)}]"
            + f" [{str(mac_address_type.created_by).ljust(10)}]"
            + f" [{str(mac_address_type.created_at).ljust(32)}]"
            + f" [{str(mac_address_type.updated_by).ljust(10)}]"
            + f" [{str(mac_address_type.updated_at).ljust(32)}]"
        )


class MacAddressTypeAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")

    def test_mac_address_type_admin_save_and_update_model(self):
        if trace_on:
            print(
                "id".ljust(5 + 3)
                + "name".ljust(30 + 3)
                + "created_by".ljust(10 + 3)
                + "created_at".ljust(32 + 3)
                + "updated_by".ljust(10 + 3)
                + "updated_at".ljust(32 + 3)
            )
        my_model_admin = MacAddressTypeAdmin(
            model=MacAddressType, admin_site=AdminSite()
        )
        self.assertEqual(str(my_model_admin), "mac_address_types.MacAddressTypeAdmin")

        mac_address_type = MacAddressType(code="NEW", name="NEW Name")
        trace(mac_address_type)
        my_model_admin.save_model(
            obj=mac_address_type, request=Mock(user=self.user), form=None, change=False
        )
        trace(mac_address_type)
        self.assertTrue(mac_address_type.created_by, self.user)
        self.assertTrue(mac_address_type.updated_by, self.user)

        mac_address_type_copy = copy.deepcopy(mac_address_type)
        mac_address_type_copy.name = mac_address_type.name + " updated"
        trace(mac_address_type_copy)
        time.sleep(0.25)
        my_model_admin.save_model(
            obj=mac_address_type_copy,
            request=Mock(user=self.user),
            form=None,
            change=True,
        )
        trace(mac_address_type_copy)

        self.assertLess(mac_address_type.created_at, mac_address_type.updated_at)
        self.assertNotEqual(mac_address_type_copy.name, mac_address_type.name)

        # mac_address_type = my_model_admin.get_object(
        #     request=Mock(user=self.user), object_id=str(1)
        # )
        # trace(mac_address_type)

        # Test CustomerAdmin active

        self.assertEqual(my_model_admin.active(mac_address_type), True)

        mac_address_type_copy = copy.deepcopy(mac_address_type)
        mac_address_type_copy.active_from = mac_address_type_copy.active_until
        # trace(mac_address)
        my_model_admin.save_model(
            obj=mac_address_type_copy,
            request=Mock(user=self.user),
            form=None,
            change=True,
        )

        self.assertEqual(my_model_admin.active(mac_address_type_copy), False)
