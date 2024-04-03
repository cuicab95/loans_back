from rest_framework import serializers
from .models import Customer, Loan, LoanPayments, RefundPayment
from django.contrib.auth.models import User


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "first_name",
            "last_name",
            "birthdate",
            "gender",
            "rfc",
            "curp",
            "contact_email",
            "phone_number",
        )
        extra_kwargs = {
            'rfc': {'min_length': 12},
            'curp': {'min_length': 18},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayments
        fields = (
            "id",
            "start_date",
            "end_date",
            "amount",
            "status",
        )


class LoanSerializer(serializers.ModelSerializer):
    customer_obj = CustomerSerializer(source="customer", read_only=True)
    adviser_obj = UserSerializer(source="adviser", read_only=True)
    load_payments = LoanPaymentSerializer(source="payments", many=True, read_only=True)

    class Meta:
        model = Loan
        fields = (
            "id",
            "customer",
            "customer_obj",
            "loan_kind",
            "amount",
            "payment_interval",
            "payment_duration",
            "interest_rate",
            "total_amount",
            "adviser",
            "adviser_obj",
            "load_payments"
        )
        extra_kwargs = {
            'adviser': {'required': False},
            'total_amount': {'required': False},
        }


class RefundPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundPayment
        fields = (
            "loan",
            "payment_date",
            "amount"
        )