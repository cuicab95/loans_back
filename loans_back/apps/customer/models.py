from django.db import models
from .catalogs import GenderChoices, LoadKindChoices, PaymentIntervalChoices, PaymentStatusChoices
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class BasicFields(models.Model):
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Customer(BasicFields):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True)
    rfc = models.CharField(max_length=13)
    curp = models.CharField(max_length=18)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Loan(BasicFields):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_kind = models.CharField(max_length=50, choices=LoadKindChoices.choices)
    amount = models.FloatField()
    payment_interval = models.CharField(max_length=10, choices=PaymentIntervalChoices.choices)
    payment_duration = models.IntegerField()
    interest_rate = models.FloatField()
    total_amount = models.FloatField()
    adviser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_loans")

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"


class LoanPayments(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.FloatField()
    status = models.CharField(
        max_length=10,
        choices=PaymentStatusChoices.choices,
        default=PaymentStatusChoices.pending
    )

    class Meta:
        verbose_name = "Loan payment"
        verbose_name_plural = "Loans payments"


class RefundPayment(BasicFields):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="refunds")
    payment_date = models.DateField()
    amount = models.FloatField()

    class Meta:
        verbose_name = "Refund payment"
        verbose_name_plural = "Refund payments"




