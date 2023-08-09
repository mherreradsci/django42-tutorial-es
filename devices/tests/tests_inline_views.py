from django.test import TestCase, Client, RequestFactory
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from devices.models import Device
from devices.forms import DeviceForm, DeviceMacAddressFormset
from devices.views import DeviceCreateView
from mac_address_types.models import MacAddressType


class DeviceTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.user.save()

        cls.number_of_devices = 0

        for id in range(0, cls.number_of_devices):
            Device.objects.create(
                code="DE" + str(id).zfill(4), name="Device " + str(id).zfill(4)
            )

        cls.mac_address_type = MacAddressType.objects.create(code="NMAT")
        cls.mac_address_type.save()

    def test_device_create_view_form_valid_success(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("devices:create")

        print("url", url)
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

        form_data = {
            "code": "XXX",
            "name": "New Device",
            "active": True,
            "active_from": timezone.now(),
            "active_until": timezone.now(),
            "macaddress_formset-TOTAL_FORMS": "0",
            "macaddress_formset-INITIAL_FORMS": "0",
            "macaddress_formset-MIN_NUM_FORMS": "0",
            "macaddress_formset-MAX_NUM_FORMS": "0",
        }

        response = self.client.post(path=url, data=form_data, follow=True)
        print("RESPONSE:", response)

        # print("response.context['form']", response.context['form'])
        # print("response.context['form'].errors", response.context['form'].errors)

        self.assertEqual(response.status_code, 200)

        # post_response = self.client.post(url, data={"submit": True}, follow=True)

        # #self.assertEqual(response.url, "/mac_address_types/list/")

        self.assertEqual(Device.objects.order_by("id").last().name, "New Device")

    # def test_device_create_view_form_valid_fail(self):
    #     result = self.client.login(username="testuser", password="password")
    #     self.assertTrue(result)

    #     url = reverse("devices:create")

    #     print("test_device_create_view_form_valid_fail:url", url)
    #     response = self.client.get(path=url)
    #     self.assertEqual(response.status_code, 200)

    #     form_data = {
    #         "code": "XXX",
    #         "name": "New Device2",
    #         "active": True,
    #         "active_from": timezone.now(),
    #         "active_until": timezone.now(),
    #     }

    #     response = self.client.post(path=url, data=form_data, follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "This field is required")

    #     print("")
    #     print ("test_device_create_view_form_valid_fail:RESPONSE:", response )
    #     print("")
    #     # print ("test_device_create_view_form_valid_fail:RESPONSE:dir(response)", dir(response))
    #     # print("")
    #     # print ("test_device_create_view_form_valid_fail:RESPONSE:response.request)", response.request)
    #     # print("")
    #     # #print("response.context['form']", response.context['form'])
    #     # #print("response.context['form'].errors", response.context['form'].errors)
    #     # print("response.context", response.context)
    #     # print("")
    #     # print("response.context_data", response.context_data)
    #     # print("")
    #     # print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWresponse.context_data")
    #     # print("response.context_data", response.context_data["formset"]["macaddress_formset"])
    #     # print("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWresponse.context_data")
    #     # #self.assertFormsetError (response=response, formset="macaddress_formset")
    #     #  #try:
    #     #self.assertFormsetError(response, formset="macaddress_formset", form_index=None, field=None, errors=[
    #     #                        "The formset 'named_formsets' was not used to render the response"])
    #     # except AssertionError as e:
    #     #     print(f"ERRORRRRRRRRRRRRRRRRRRRRRRRRRRR[{e}]")
    #     #     self.assertDictContainsSubset(e, "The formset \'named_formsets\' was not used to render the response")

    #     print("")

    #     #print("response.content", response.content)
    #     print("")

    #     # post_response = self.client.post(url, data={"submit": True}, follow=True)

    #     # #self.assertEqual(response.url, "/mac_address_types/list/")

    #     # self.assertEqual(Device.objects.order_by("id").last().name, "New Device")
