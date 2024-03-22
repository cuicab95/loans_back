from factory.django import DjangoModelFactory
from .models import Customer, Loan


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer


class LoanFactory(DjangoModelFactory):
    class Meta:
        model = Loan
