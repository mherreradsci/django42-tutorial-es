from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from devices.models import Device
from devices.forms import DeviceMacAddressFormset

from accounts.models import User
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


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.user.save()

        cls.number_of_devices = 50

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()

        fisrt_device = Device.objects.order_by("id").first()
        print("PPPPPPPPPPPPPP::fisrt_device:", fisrt_device)

        cls.ma = MacAddress.objects.create(
            address="werwerwqerqwer",
            maad_type=cls.mac_address_type,
            device=fisrt_device,
        )
        cls.ma.save()

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

    # def test_device_create_view_get_initial(self):
    #     result = self.client.login(username="testuser", password="password")
    #     self.assertTrue(result)

    #     url = reverse("devices:create")
    #     print("YYYYYYYYYYYYY:test_device_create_view_get_initial:url::", url)
    #     # form_data = {"code": "NEW", "name": "New Device"}

    #     form_data = {
    #         "code": "NEW",
    #         "name": "New Device",
    #         "active": True,
    #         "active_from": timezone.now(),
    #         "active_until": timezone.now(),
    #         "created_by": self.user,
    #         "updated_by": self.user,
    #         "macaddress_set-TOTAL_FORMS": "0",
    #         "macaddress_set-INITIAL_FORMS": "0",
    #         "macaddress_set-MAX_NUM_FORMS": "0",
    #     }

    #     response = self.client.post(path=url, data=form_data, follow=True)
    #     # self.assertEqual(Device.objects.last().name, "New Device")

    #     # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response::", response)
    #     # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response.context::", response.context)
    #     # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response.redirect_chain:", response.redirect_chain)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(
    #         response.template_name, ["devices/device_create_or_update.html"]
    #     )

    # def test_XXXXXXXXXXXXXXXXXX(self):
    #     result = self.client.login(username="testuser", password="password")
    #     self.assertTrue(result)

    #     url = reverse("devices:create")

    #     request = self.client.get(path=url)
    #     request.user = self.user
    #     form_data = {
    #         "code": "XXX",
    #         "name": "New Device",
    #         "active": True,
    #         "active_from": timezone.now(),
    #         "active_until": timezone.now(),
    #     }

    #     #request.data = form_data

    #     response = DeviceCreateView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)

    #     print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:response:", response)
    #     print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:response.context_data[form]:", response.context_data["form"])

    #     form_data = {
    #         "code": "XXX",
    #         "name": "New Device",
    #         "active": True,
    #         "active_from": timezone.now(),
    #         "active_until": timezone.now(),
    #     }
    #     response = self.client.post(path=url, data=form_data)
    #     print ("RESPONSE:", response )

    #     print("response.context['form']", response.context['form'])
    #     print("response.context['form'].errors", response.context['form'].errors)

    #     self.assertEqual(response.status_code, 302)

    #     #self.assertEqual(response.url, "/mac_address_types/list/")

    #     self.assertEqual(Device.objects.order_by("id").last().name, "New MacAddressType")

    # def test_device_create_view_form_valid(self):
    #     result = self.client.login(username="testuser", password="password")
    #     self.assertTrue(result)

    #     url = reverse("devices:create")
    #     print("YYYYYYYYYYYYY:test_device_create_view_get_initial:url::", url)

    #     request = self.factory.get(url)
    #     request.session = self.client.session
    #     request.user = self.user

    #     response = DeviceCreateView.as_view()(request)

    #     print("#################################dir(response):", dir(response))

    #     print("#################################:request.POST:", request.POST)

    #     self.assertEqual(response.status_code, 200)

    #     data = {
    #         "code": "NEW",
    #         "name": "New Devicex",
    #         "active": True,
    #         "active_from": timezone.now(),
    #         "active_until": timezone.now(),
    #         "created_by": self.user,
    #         "updated_by": self.user,
    #         "macaddress_set-TOTAL_FORMS": "0",
    #         "macaddress_set-INITIAL_FORMS": "0",
    #         "macaddress_set-MAX_NUM_FORMS": "0",

    #     }

    #     form = DeviceForm(data)
    #     self.assertTrue(form.is_valid())
    #     #response = self.client.get(url, data)
    #     response = self.factory.post(url, data)
    #     # print("\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz:reponse:\n", response )
    #     # print("\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz:response.request:\n", response.request )
    #     # print("\nzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz:reponse.reason_phrase:\n", response.reason_phrase )

    #     self.assertEqual(Device.objects.order_by("id").last().name, "New Device")

    #     # #self.assertEqual(response.status_code, 302)
    #     # #self.assertRedirects(response, reverse("accounts:login"))

    #     # #form_data = {"code": "NEW", "name": "New Device"}

    #     # # response = self.client.post(path=url, data=form_data, follow=True)
    #     # # self.assertEqual(Device.objects.last().name, "New Device")

    #     # # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response::", response)
    #     # # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response.context::", response.context)
    #     # # print("YYYYYYYYYYYYY:test_device_create_view_get_initial:response.redirect_chain:", response.redirect_chain)
    #     # # self.assertEqual(response.status_code, 200)
    #     # # self.assertEqual(
    #     # #     response.template_name, ["devices/device_create_or_update.html"]
    #     # # )

    def test_device_update_view_formset(self):
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
            "macaddress_formset-TOTAL_FORMS": "0",
            "macaddress_formset-INITIAL_FORMS": "0",
            "macaddress_formset-MIN_NUM_FORMS": "0",
            "macaddress_formset-MAX_NUM_FORMS": "0",
        }

        response = self.client.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 302)

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
