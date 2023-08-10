from accounts.models import User
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from mac_address_types.models import MacAddressType


class MacAddressTypeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")

        cls.number_of_mac_address_types = 50

        for id in range(0, cls.number_of_mac_address_types):
            MacAddressType.objects.create(
                code="MA" + str(id).zfill(4), name="MacAddressType " + str(id).zfill(4)
            )

    def test_macaddresstype_list_view_get_queryset(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get("/mac_address_types/list/", **headers)
        self.assertEqual(response.status_code, 200)  # check 200 OK response

        clients = response.context

        self.assertEqual(
            len(clients["macaddresstype_list"]), clients["view"].paginate_by
        )

    def test_macaddresstype_list_view_get_queryset_filtered(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)
        response = self.client.get("/mac_address_types/list/?q=0000")

        self.assertEqual(
            response.template_name, "mac_address_types/macaddresstype_list.html"
        )
        self.assertEqual(response.context_data["paginator"].count, 1)

        self.assertEqual(response.status_code, 200)

    def test_mac_address_type_create_view_get_initial(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("mac_address_types:create")
        form_data = {"code": "NEW", "name": "New MacAddressType"}
        response = self.client.post(path=url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/mac_address_types/list/")

        self.assertEqual(
            MacAddressType.objects.order_by("id").last().name, "New MacAddressType"
        )

    def test_mac_address_type_update_view(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = MacAddressType.objects.all().first()

        url = reverse("mac_address_types:update", kwargs={"pk": object.pk})

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
        self.assertEqual(response.status_code, 302)

    def test_mac_address_type_delete_view_get_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        qs = MacAddressType.objects.all()
        object = qs.first()

        url = reverse("mac_address_types:delete", args=(object.id,))

        response = self.client.get(url, follow=True)

        self.assertContains(response, "Are you sure you want to delete ")
        self.assertEqual(
            response.template_name[0],
            "mac_address_types/macaddresstype_confirm_delete.html",
        )
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(url, data={"cancel": True}, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.template_name, "mac_address_types/macaddresstype_list.html"
        )

    def test_mac_address_type_delete_view_post_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = MacAddressType.objects.all().first()
        url = reverse("mac_address_types:delete", args=(object.id,))

        post_response = self.client.post(url, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(
            post_response.template_name, "mac_address_types/macaddresstype_list.html"
        )
        self.assertEqual(
            len(post_response.context["macaddresstype_list"]),
            post_response.context["view"].paginate_by,
        )
