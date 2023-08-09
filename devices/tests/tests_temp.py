from accounts.models import User
from django.test import TestCase, Client, RequestFactory
from django.forms.models import inlineformset_factory
from django.urls import reverse
from django.utils import timezone

from devices.models import Device
from devices.forms import DeviceMacAddressFormset
from mac_address_types.models import MacAddressType
from mac_addresses.models import MacAddress


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

        cls.ma = MacAddress.objects.create(
            address="werwerwqerqwer",
            maad_type=cls.mac_address_type,
            device=cls.first_device,
        )
        cls.ma.save()

        cls.ma_count = MacAddress.objects.count()
        print("PPPPPPPPPPPPPP:ma_count:", cls.ma_count)

    def test_device_update_view_without_formset(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Device.objects.order_by("id").first()
        print(
            "test_device_update_view_without_formset:QQQQQQQQQQQQQQQQQQQQQQ:object:",
            object,
        )

        # ma = MacAddress.objects.create(
        #     address="werwerwqerqwer",  maad_type=self.mac_address_type,
        #     device=object)
        # ma.save()

        url = reverse("devices:update", kwargs={"pk": object.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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

        url = reverse("devices:update", kwargs={"pk": object.pk})
        form_data = {
            "code": object.code,
            "name": object.name,
            "active": object.active,
            "active_from": object.active_from,
            "active_until": object.active_until,
            "created_by": self.user,
            "updated_by": self.user,
            "macaddress_set-TOTAL_FORMS": "1",
            "macaddress_set-INITIAL_FORMS": "1",
            "macaddress_set-MIN_NUM_FORMS": "0",
            "macaddress_set-MAX_NUM_FORMS": "",
            "macaddress_set-0-address": "NEW MAC ADDRESS",
            "macaddress_set-0-maad_type": "1",  # self.ma.maad_type,
            "macaddress_set-0-active": "1",
            "macaddress_set-0-active_from": timezone.now(),
            # "initial-macaddress_formset-0-active_from" : timezone.now(),
            "macaddress_set-0-active_until": timezone.now(),
            "macaddress_set-0-created_by": self.user,
            "macaddress_set-0-updated_by": self.user,
            # "macaddress_set-0-DELETE"             :"0",
            "macaddress_set-0-id": "1",
            # "macaddress_set-0-device"            :self.ma # :self.first_device
        }
        formset = DeviceMacAddressFormset(form_data)
        print(
            "test_device_update_view_without_formset:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset:",
            formset,
        )
        print(
            "test_device_update_view_without_formset:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.errors:",
            formset.errors,
        )
        print(
            "test_device_update_view_without_formset:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:dir(formset.errors):",
            dir(formset.errors),
        )
        # self.assertEqual(len(formset.errors), 0)
        print(
            "test_device_update_view_without_formset:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.non_form_errors():",
            formset.non_form_errors(),
        )
        print(
            "test_device_update_view_without_formset:GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG:formset.total_error_count():",
            formset.total_error_count(),
        )

        # self.assertEqual(formset.total_error_count(), 0)
        self.assertTrue(formset.is_valid())

        response = self.client.post(path=url, data=form_data)
        self.assertEqual(response.status_code, 302)

        # ma = MacAddress.objects.order_by("id").first()
        self.ma.refresh_from_db()
        print(
            "test_device_update_view_without_formset:$$$$$$$$$$$$$$$$$$$$$$$$$:ma.id:",
            self.ma.id,
        )
        print(
            "test_device_update_view_without_formset:$$$$$$$$$$$$$$$$$$$$$$$$$:ma.ADDRESS:",
            self.ma.address,
        )
        print(
            "test_device_update_view_without_formset:$$$$$$$$$$$$$$$$$$$$$$$$$:ma.device:",
            self.ma.device,
        )

        ma_count = MacAddress.objects.count()
        print(
            "test_device_update_view_without_formset:$$$$$$$$$$$$$$$$$$$$$$$$$:ma_count:",
            ma_count,
        )

        self.assertEqual(self.ma.address, "NEW MAC ADDRESS")

        self.assertEqual(response.url, reverse("devices:list"))

        # form_data = {
        #     "code": object.code,
        #     "name": object.name,
        #     "active": object.active,
        #     "active_from": object.active_from,
        #     "active_until": object.active_until,
        #     "created_by": self.user,
        #     "updated_by": self.user,
        #     "macaddress_set-TOTAL_FORMS": "1",
        #     "macaddress_set-INITIAL_FORMS": "0",
        #     "macaddress_set-MIN_NUM_FORMS": "0",
        #     "macaddress_set-MAX_NUM_FORMS": "1000",
        #     "macaddress_set-0-address": self.ma,
        #     "macaddress_set-0-maad_type": self.ma.maad_type,

        # "macaddress_formset-TOTAL_FORMS"
        # "macaddress_formset-INITIAL_FORMS"
        # "macaddress_formset-MIN_NUM_FORMS"
        # "macaddress_formset-MAX_NUM_FORMS"
        # "macaddress_formset-0-address"
        # "macaddress_formset-0-maad_type"
        # "macaddress_formset-0-active"
        # "macaddress_formset-0-active_from"
        # "initial-macaddress_formset-0-active_from"
        # "macaddress_formset-0-active_until"
        # "macaddress_formset-0-created_by"
        # "macaddress_formset-0-updated_by"
        # "macaddress_formset-0-DELETE"
        # "macaddress_formset-0-id"
        # "macaddress_formset-0-device"
