from rest_framework.test import APITestCase
from loans_back.apps.customer.factories import CustomerFactory
from django.contrib.auth.models import User
from rest_framework_simplejwt.settings import api_settings
from loans_back.apps.customer.catalogs import GenderChoices


class LoanConfigTest(APITestCase):
    def create_customer(self, first_name=None, last_name=None):
        kwargs = {
            "first_name": "Carlos" if not first_name else first_name,
            "last_name": "Uicab" if not last_name else last_name,
            "birthdate": "1995-12-27",
            "gender": GenderChoices.man,
            "rfc": "RFC123456712",
            "curp": "CURP12345678901234",
            "contact_email": "test2@example.com",
            "phone_number": "+529999999999"
        }
        return CustomerFactory(**kwargs)

    def create_user(
        self,
        username="root",
        password="test",
        **kwargs,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            **kwargs
        )
        return user

    def update_token(self, token):
        auth = f"{api_settings.AUTH_HEADER_TYPES[0]} {token}"
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def authenticate(self, user, password=None):
        password = password or "test"
        user = user.username if isinstance(user, User) else user
        response = self.client.post(
            "/security/api/token/", {"username": user, "password": password}
        )
        if response.status_code == 200:
            self.update_token(response.json().get("access"))
        return response

