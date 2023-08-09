from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from accounts.models import User
from devices.models import Device
from devices.forms import DeviceMacAddressFormset
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress


from django.utils import timezone


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

        cls.first_device = Device.objects.order_by("id").first()
        print("PPPPPPPPPPPPPP::first_device:", cls.first_device)

        # cls.ma = MacAddress.objects.create(
        #     address="werwerwqerqwer",  maad_type=cls.mac_address_type,
        #     device=cls.first_device)
        # cls.ma.save()

        cls.ma_count = MacAddress.objects.count()
        print("PPPPPPPPPPPPPP:ma_count:", cls.ma_count)

    def test_device_create_view(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        # object = Device.objects.order_by("id").first()
        # print(
        #     "test_device_create_view:QQQQQQQQQQQQQQQQQQQQQQ:object:", object)

        # ma = MacAddress.objects.create(
        #     address="werwerwqerqwer",  maad_type=self.mac_address_type,
        #     device=object)
        # ma.save()

        url = reverse("devices:create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, MacAddress.objects.count())

        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
        # print(response.context)
        print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

        # data = {}

        # # global information, some additional fields may go there
        # data['csrf_token'] = response.context['csrf_token']

        # # management form information, needed because of the formset
        # management_form = response.context['form'].management_form
        # for i in 'TOTAL_FORMS', 'INITIAL_FORMS', 'MIN_NUM_FORMS', 'MAX_NUM_FORMS':
        #     data['%s-%s' % (management_form.prefix, i)] = management_form[i].value()

        form_data = {
            "code": "123456",
            # "name": "NEW DEV NAME",
            # "active": True,
            # "active_from": timezone.now(),
            # "active_until": timezone.now(),
            # "created_by": self.user,
            # "updated_by": self.user,
            "macaddress_set-TOTAL_FORMS": "1",
            "macaddress_set-INITIAL_FORMS": "0",
            "macaddress_set-MIN_NUM_FORMS": "0",
            "macaddress_set-MAX_NUM_FORMS": "",
            "macaddress_set-0-address": "NEW MAC ADDRESS",
            "macaddress_set-0-maad_type": "1",  # self.ma.maad_type,
            # "macaddress_set-0-active"              : "1",
            # "macaddress_set-0-active_from" : timezone.now(),
            # #"initial-macaddress_formset-0-active_from" : timezone.now(),
            # "macaddress_set-0-active_until"       : timezone.now(),
            # "macaddress_set-0-created_by"         :self.user,
            # "macaddress_set-0-updated_by"         :self.user,
            "macaddress_set-0-DELETE": False,
            # "macaddress_set-0-id"                 :None
            # "macaddress_set-0-device"            :self.ma # :self.first_device
        }
        formset = DeviceMacAddressFormset(form_data)
        print(
            "test_device_create_view:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset:", formset
        )
        print(
            "test_device_create_view:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.errors:",
            formset.errors,
        )
        print(
            "test_device_create_view:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:dir(formset.errors):",
            dir(formset.errors),
        )
        # self.assertEqual(len(formset.errors), 0)
        print(
            "test_device_create_view:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.non_form_errors():",
            formset.non_form_errors(),
        )
        print(
            "test_device_create_view:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.total_error_count():",
            formset.total_error_count(),
        )

        # self.assertEqual(formset.total_error_count(), 0)
        self.assertTrue(formset.is_valid())

        response = self.client.post(path=url, data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

        print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:response:", response)
        # print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:response.context:", response.context["errors"])

        de = Device.objects.order_by("id").last()
        print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:de:", de)
        self.assertEqual(de.code, "123456")

        ma = MacAddress.objects.order_by("id").first()
        # #self.ma.refresh_from_db()
        print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:ma:", ma)
        # print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:ma.ADDRESS:", ma.address)
        # print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:ma.device:", ma.device)

        ma_count = MacAddress.objects.count()
        print("test_device_create_view:$$$$$$$$$$$$$$$$$$$$$$$$$:ma_count:", ma_count)

        self.assertEqual(ma_count, 1)

        # self.assertEqual(response.url, reverse("devices:list"))

        # Check that form_valid has been called.
        self.assertRedirects(response, reverse("devices:list"))
