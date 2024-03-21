from loans_back.config.tests import LoanConfigTest
from loans_back.apps.customer.catalogs import GenderChoices
from rest_framework import status


class CustomerTestCase(LoanConfigTest):
    def setUp(self):
        self.user = self.create_user()
        self.customer = self.create_customer(first_name="Pedro", last_name="Aguilar")
        self.customer_2 = self.create_customer(first_name="Juanito", last_name="Perez")
        self.path = "/customer/customer/"
        self.authenticate(self.user)

    def test_customer_list(self):
        response = self.client.get(f"{self.path}")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), 2)

    def test_customer_create(self):
        data_request = {
            "first_name": "Ana",
            "last_name": "Hernandez",
            "birthdate": "1974-01-27",
            "gender": GenderChoices.women,
            "rfc": "RFC123456712",
            "curp": "CURP12345678901234",
            "contact_email": "test2@example.com",
            "phone_number": "+529993458976"
        }
        response = self.client.post(f"{self.path}", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer_create_with_error(self):
        """
        RFC: this field has at least 12 characters
        CURP: this field has at least 18 characters
        """
        data_request = {
            "first_name": "Ana",
            "last_name": "Hernandez",
            "birthdate": "1974-01-27",
            "gender": GenderChoices.women,
            "rfc": "RFC",
            "curp": "CURP",
            "contact_email": "test2@example.com",
            "phone_number": "+529993458976"
        }
        response = self.client.post(f"{self.path}", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_retrieve(self):
        response = self.client.get(f"{self.path}{self.customer.id}/")
        data = response.data
        self.assertEqual(data["first_name"], self.customer.first_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_delete(self):
        response = self.client.delete(f"{self.path}{self.customer.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_update(self):
        data_request = {
            "first_name": "Gabriela",
            "last_name": "Perez",
        }
        response = self.client.patch(f"{self.path}{self.customer_2.id}/", data=data_request)
        self.assertNotEqual(response.data["first_name"], self.customer_2.first_name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
