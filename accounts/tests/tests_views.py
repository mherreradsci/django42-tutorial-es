from http import HTTPStatus

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from accounts import views
from accounts.forms import CustomAuthForm, CustomUserCreationForm
from accounts.models import User


class AutenticationViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username="testuser", password="password", email="testuser@example.com"
        )

    def test_login_view_successful(self):
        url = reverse("accounts:login")
        request = self.factory.post(url)
        request.user = self.user
        request.session = self.client.session

        data = {
            "username": "testuser",
            "password": "password",
        }
        form = CustomAuthForm(request, data)
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302
        self.assertRedirects(response, reverse("customers:list"))

    def test_login_view_redirect_successful(self):
        url = reverse("accounts:login")
        request = self.factory.post(url)
        request.user = self.user
        request.session = self.client.session
        # response = views.logout_view(request)

        data = {
            "username": "testuser",
            "password": "password",
            "next": "/devices/list/",
        }
        form = CustomAuthForm(request, data)

        self.assertTrue(form.is_valid())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("devices:list"))

    def test_logout_view_from_logged_user(self):
        self.client = Client()
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

        url = reverse("accounts:logout")
        request = self.factory.post(url)
        request.user = self.user
        request.session = self.client.session
        response = views.logout_view(request)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, "/accounts/login/")

    def test_logout_view_from_not_logged_user(self):
        self.client = Client()
        url = reverse("accounts:logout")
        request = self.factory.get(url)
        request.user = self.user
        request.session = self.client.session
        response = views.logout_view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_view_successful(self):
        url = reverse("accounts:register")
        request = self.factory.get(url)
        request.session = self.client.session

        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = CustomUserCreationForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_register_view_unsuccessful(self):
        url = reverse("accounts:register")
        request = self.factory.get(url)
        request.session = self.client.session

        data = {
            "username": "testuser",
            "email": "newuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        form = CustomUserCreationForm(data)
        self.assertFalse(form.is_valid())
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
