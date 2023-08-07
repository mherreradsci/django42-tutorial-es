from accounts.models import User
from django.test import TestCase, Client, RequestFactory
from django.forms.models import inlineformset_factory
from django.urls import reverse
from .models import Device
from .forms import DeviceForm, DeviceMacAddressFormset
from .views import DeviceCreateView
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress


# class DeletionTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.factory = RequestFactory()
#         cls.client = Client()

#         # Create an user for login
#         cls.user = User.objects.create(
#             username="testuser", password="password")

#         # cls.number_of_devices = 50

#         # for id in range(0, cls.number_of_devices):
#         #     Device.objects.create(
#         #         code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
#         #     )

#         cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
#         cls.mac_address_type.save()

#     def test_deletion(self):

#         DeviceMacAddressFormset = inlineformset_factory(
#             Device,
#             MacAddress,
#             fields=[
#                 "address",
#                 "maad_type",
#             ],
#             extra=0,
#             can_delete=True,
#         )

#         device = Device.objects.create(code='test', name="test")
#         mac_address = MacAddress.objects.create(address= '00-00-00-00-00-00',
#                                         maad_type=self.mac_address_type,
#                                         device = device)

#         data = {
#             "macaddress_set-TOTAL_FORMS": "1",
#             "macaddress_set-INITIAL_FORMS": "1",
#             "macaddress_set-MAX_NUM_FORMS": "0",
#             "macaddress_set-0-id": str(device.pk),
#             "macaddress_set-0-poet": str(mac_address.pk),
#             "macaddress_set-0-address": "test",
#             "macaddress_set-0-DELETE": "on",
#         }
#         formset = DeviceMacAddressFormset(data, instance=device)
#         formset.save()
#         self.assertTrue(formset.is_valid())
#         self.assertEqual(MacAddress.objects.count(), 0)

from django.utils import timezone


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")

        cls.number_of_devices = 50

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()

    def test_device_list_view_get_queryset(self):
        result = self.client.login(username="testuser", password="password")

        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get("/devices/list/", **headers)
        self.assertEqual(response.status_code, 200)  # check 200 OK response

        clients = response.context

        self.assertEqual(len(clients["device_list"]), clients["view"].paginate_by)

    def test_device_list_view_get_queryset_filtered(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)
        response = self.client.get("/devices/list/?q=0000")

        self.assertEqual(response.template_name, "devices/device_list.html")
        self.assertEqual(response.context_data["paginator"].count, 1)

        self.assertEqual(response.status_code, 200)

    def test_device_create_view_get_initial(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("devices:create")
        form_data = {"code": "NEW", "name": "New Device"}
        response = self.client.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.template_name, ["devices/device_create_or_update.html"]
        )

    def test_device_update_view(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Device.objects.all().first()

        url = reverse("devices:update", kwargs={"pk": object.pk})

        form_data = {
            "code": object.code,
            "name": object.name,
            "active": object.active,
            "active_from": object.active_from,
            "active_until": object.active_until,
            "created_by": self.user,
            "updated_by": self.user,
        }

        response = self.client.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_device_delete_view_get_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        qs = Device.objects.all()
        object = qs.first()

        url = reverse("devices:delete", args=(object.id,))

        response = self.client.get(url, follow=True)

        self.assertContains(response, "Are you sure you want to delete ")
        self.assertEqual(
            response.template_name[0], "devices/device_confirm_delete.html"
        )
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(url, data={"cancel": True}, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.template_name, "devices/device_list.html")

    def test_device_delete_view_post_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Device.objects.all().first()
        url = reverse("devices:delete", args=(object.id,))

        post_response = self.client.post(url, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.template_name, "devices/device_list.html")
        self.assertEqual(
            len(post_response.context["device_list"]),
            post_response.context["view"].paginate_by,
        )
