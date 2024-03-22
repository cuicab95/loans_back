from loans_back.config.tests import LoanConfigTest
from loans_back.apps.customer.catalogs import GenderChoices, LoadKindChoices, PaymentIntervalChoices, PaymentStatusChoices
from rest_framework import status
from .messages import ERROR_LOAN_PAYMENT_PAID


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


class LoanTestCase(LoanConfigTest):
    def setUp(self):
        self.user = self.create_user()
        self.customer = self.create_customer(first_name="Pedro", last_name="Aguilar")
        self.customer_2 = self.create_customer(first_name="Miguel", last_name="Tun")
        self.path = "/customer/loan/"
        self.authenticate(self.user)
        self.loan = self.create_loan(self.customer, self.user)
        self.loan_2 = self.create_loan(self.customer_2, self.user)

    def test_customer_list(self):
        response = self.client.get(f"{self.path}")
        data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data.get("results")), 2)

    def test_customer_retrieve(self):
        response = self.client.get(f"{self.path}{self.loan.id}/")
        data = response.data
        self.assertEqual(data["customer"], self.customer.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_create(self):
        data_request = {
            "customer": self.customer.id,
            "loan_kind": LoadKindChoices.debt_payment,
            "amount": 30000,
            "payment_interval": PaymentIntervalChoices.month,
            "payment_duration": 12,
            "interest_rate": 30
        }
        response = self.client.post(f"{self.path}", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payments = response.data.get('load_payments', [])
        sum_payments = sum(map(lambda x: x['amount'], payments))
        self.assertEqual(sum_payments, response.data.get('total_amount'))

    def test_customer_delete(self):
        response = self.client.delete(f"{self.path}{self.loan.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_loan_update(self):
        data_request = {
            "loan_kind": LoadKindChoices.education,
            "amount": 7500,
            "payment_interval": PaymentIntervalChoices.year,
            "payment_duration": 5,
            "interest_rate": 35
        }
        response = self.client.patch(f"{self.path}{self.loan.id}/", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('interest_rate'), self.loan.interest_rate)
        self.assertNotEqual(response.data.get('amount'), self.loan.amount)
        payments = response.data.get('load_payments', [])
        sum_payments = sum(map(lambda x: x['amount'], payments))
        self.assertEqual(sum_payments, response.data.get('total_amount'))

    def test_error_loan_update_with_payment_paid(self):
        loan_payment = self.loan.payments.first()
        loan_payment.status = PaymentStatusChoices.paid
        loan_payment.save()
        data_request = {
            "loan_kind": LoadKindChoices.education,
            "amount": 7500,
            "payment_interval": PaymentIntervalChoices.year,
            "payment_duration": 5,
            "interest_rate": 35
        }
        response = self.client.patch(f"{self.path}{self.loan.id}/", data=data_request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], ERROR_LOAN_PAYMENT_PAID)
