from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from accounts.models import User
from customers.models import Customer


class CustomerTest(TestCase):
    """Test for Customer Views"""

    @classmethod
    def setUpTestData(cls):
        # Every test needs access to the request factory.
        # headers = {"HTTP_HX-Request": "true"}
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create an user for login
        cls.user = User.objects.create_user(username="testuser", password="password")

        # User.objects.create(username="init")
        cls.number_of_customers = 15

        for id in range(0, cls.number_of_customers):
            Customer.objects.create(
                code="CR" + str(id).zfill(4), name="Cliente " + str(id).zfill(4)
            )

    def test_customer_list_view_get_queryset(self):
        # Create an instance of a POST request.
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        headers = {"HTTP_HX-Request": "true"}
        response = self.client.get("/customers/list/", **headers)
        self.assertEqual(response.status_code, 200)  # check 200 OK response

        clients = response.context

        self.assertEqual(len(clients["customer_list"]), clients["view"].paginate_by)

    def test_customer_list_view_get_queryset_filtered(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)
        response = self.client.get("/customers/list/?q=CR0000")
        self.assertEqual(response.status_code, 200)

    def test_customer_create_view_get_initial(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        url = reverse("customers:create")

        form_data = {"code": "CUS001", "name": "Customer 001"}
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/customers/list/")

    def test_customer_update_view(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Customer.objects.all().first()

        url = reverse("customers:update", kwargs={"pk": object.pk})

        form_data = {
            "code": object.code,
            "name": object.name,
            "active": object.active,
            "active_from": object.active_from,
            "active_until": object.active_until,
            "created_by": self.user,
            "updated_by": self.user,
        }

        response = self.client.post(url, form_data)

        # successful update: 302::='Found'
        self.assertEqual(response.status_code, 302)

    def test_customer_delete_view_get_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        qs = Customer.objects.all()
        object = qs.first()

        url = reverse("customers:delete", args=(object.id,))

        response = self.client.get(url, follow=True)
        self.assertContains(response, "Are you sure you want to delete ")
        self.assertEqual(
            response.template_name[0], "customers/customer_confirm_delete.html"
        )
        self.assertEqual(response.status_code, 200)

        post_response = self.client.post(url, data={"cancel": True}, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.template_name, "customers/customer_list.html")

    def test_customer_delete_view_post_request(self):
        result = self.client.login(username="testuser", password="password")
        self.assertTrue(result)

        object = Customer.objects.all().first()

        url = reverse("customers:delete", args=(object.id,))

        post_response = self.client.post(url, follow=True)

        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.template_name, "customers/customer_list.html")
        self.assertEqual(
            len(post_response.context["customer_list"]),
            post_response.context["view"].paginate_by,
        )
