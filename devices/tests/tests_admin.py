from django.test import TestCase
from unittest.mock import Mock
import copy

from django.contrib.admin.sites import AdminSite
from accounts.models import User
from devices.models import Device
from devices.admin import DeviceAdmin


trace_on = False


def trace(device):
    if trace_on:
        print(
            f"[{str(device.id).ljust(5)}]"
            + f" [{device.name.ljust(30)}]"
            + f" [{str(device.created_by).ljust(10)}]"
            + f" [{str(device.created_at).ljust(32)}]"
            + f" [{str(device.updated_by).ljust(10)}]"
            + f" [{str(device.updated_at).ljust(32)}]"
        )


class DeviceAdminTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password")

    def test_device_admin_save_and_update_model(self):
        if trace_on:
            print(
                f"id".ljust(5 + 3)
                + f"name".ljust(30 + 3)
                + f"created_by".ljust(10 + 3)
                + f"created_at".ljust(32 + 3)
                + f"updated_by".ljust(10 + 3)
                + f"updated_at".ljust(32 + 3)
            )
        my_model_admin = DeviceAdmin(model=Device, admin_site=AdminSite())
        self.assertEqual(str(my_model_admin), "devices.DeviceAdmin")

        device = Device(code="DeviceX", name="Nombre DeviceX")
        trace(device)
        my_model_admin.save_model(
            obj=device, request=Mock(user=self.user), form=None, change=False
        )
        trace(device)
        self.assertTrue(device.created_by, self.user)
        self.assertTrue(device.updated_by, self.user)

        # device_name_saved = device.name
        device_copy = copy.deepcopy(device)
        device_copy.name = device.name + " updated"
        # trace(device)
        my_model_admin.save_model(
            obj=device_copy, request=Mock(user=self.user), form=None, change=True
        )
        trace(device)

        self.assertLess(device.created_at, device.updated_at)
        self.assertNotEqual(device_copy.name, device.name)

        # device = my_model_admin.get_object(
        #     request=Mock(user=self.user), object_id=str(1)
        # )
        # trace(device)
