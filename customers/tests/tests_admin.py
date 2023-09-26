from unittest.mock import Mock

from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from accounts.models import User
from customers.admin import CustomerAdmin
from customers.models import Customer
from devices.models import Device, DeviCustAssignment
from devices_assignments.forms import DeviCustAssignmentFormset


class MockRequest:
    pass


class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            username="user01",
            password="passwordXrtfn123",
            email="testclient@example.com",
            is_active=True,
        )
        cls.u1.save()

        cls.u2 = User.objects.create_user(
            username="user02",
            password="passwordXrtfn123",
            email="testclient@example.com",
            is_active=True,
        )
        cls.u2.save()

        cls.customer = Customer.objects.create(
            code="CUST01",
            name="Name CUST01",
        )
        cls.customer.save()

        cls.customer02 = Customer.objects.create(
            code="CUST02",
            name="Name CUST02",
        )
        cls.customer02.save()

        cls.device = Device.objects.create(
            code="DEV001",
            name="Device 001",
        )
        cls.device.save()

        cls.device02 = Device.objects.create(
            code="DEV002",
            name="Device 002",
        )
        cls.device02.save()

        cls.dca = DeviCustAssignment.objects.create(
            customer=cls.customer, device=cls.device
        )
        cls.dca.save()

    # def setUp(self):
    #     self.site = AdminSite()

    def test_model_admin_save_formset_create(self):
        # ma = ModelAdmin(Customer, self.site)
        # self.assertEqual(str(ma), "customers.ModelAdmin")
        data = {
            "devicustassignment_set-TOTAL_FORMS": 1,
            "devicustassignment_set-INITIAL_FORMS": 0,
            "devicustassignment_set-MAX_NUM_FORMS": 1000,
            "devicustassignment_set-0-device": self.device02,
            "devicustassignment_set-0-active": "1",
            "devicustassignment_set-0-created_by": self.u1,
            "devicustassignment_set-0-updated_by": self.u1,
            "devicustassignment_set-0-id": "",
        }
        formset = DeviCustAssignmentFormset(
            data, instance=self.customer  # , prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        my_model_admin = CustomerAdmin(model=Customer, admin_site=AdminSite())
        request = MockRequest()
        request.user = self.u1

        my_model_admin.save_formset(request, form=None, formset=formset, change=True)
        qs = DeviCustAssignment.objects.filter(customer=self.customer)

        count = qs.count()

        self.assertEqual(count, 2)

    def test_model_admin_save_update(self):
        my_model_admin = CustomerAdmin(model=Customer, admin_site=AdminSite())

        self.customer.name = "EUREKA"
        my_model_admin.save_model(
            obj=self.customer, request=Mock(user=self.u1), form=None, change=True
        )

        customer = Customer.objects.get(code="CUST01")
        self.assertEqual(customer.name, "EUREKA")

    def test_model_admin_save_formset_update(self):
        data = {
            "devicustassignment_set-TOTAL_FORMS": 1,
            "devicustassignment_set-INITIAL_FORMS": 1,
            "devicustassignment_set-MAX_NUM_FORMS": 1000,
            "devicustassignment_set-0-device": self.device02,
            # "devicustassignment_set-0-active": "",
            "devicustassignment_set-0-active_from": "2400-01-01 00:00:00",
            "devicustassignment_set-0-created_by": self.u1,
            "devicustassignment_set-0-updated_by": self.u1,
            "devicustassignment_set-0-id": "1",
        }
        formset = DeviCustAssignmentFormset(
            data, instance=self.customer  # , prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        my_model_admin = CustomerAdmin(model=Customer, admin_site=AdminSite())
        request = MockRequest()
        request.user = self.u1

        my_model_admin.save_formset(request, form=None, formset=formset, change=True)
        qs = DeviCustAssignment.objects.filter(
            customer=self.customer, device=self.device02
        )

        count = qs.count()

        self.assertEqual(count, 1)
        self.assertEqual(qs.first().active, False)

    def test_model_admin_save_formset_delete(self):
        data = {
            "devicustassignment_set-TOTAL_FORMS": 1,
            "devicustassignment_set-INITIAL_FORMS": 1,
            "devicustassignment_set-MAX_NUM_FORMS": 1000,
            "devicustassignment_set-0-device": self.device02,
            "devicustassignment_set-0-active": "",
            "devicustassignment_set-0-created_by": self.u1,
            "devicustassignment_set-0-updated_by": self.u1,
            "devicustassignment_set-0-id": "1",
            "devicustassignment_set-0-DELETE": True,
        }
        formset = DeviCustAssignmentFormset(
            data, instance=self.customer  # , prefix="assignments"
        )

        self.assertEqual(formset.is_valid(), True)

        my_model_admin = CustomerAdmin(model=Customer, admin_site=AdminSite())
        request = MockRequest()
        request.user = self.u1

        my_model_admin.save_formset(request, form=None, formset=formset, change=True)
        qs = DeviCustAssignment.objects.filter(
            customer=self.customer, device=self.device02
        )

        count = qs.count()

        self.assertEqual(count, 0)
