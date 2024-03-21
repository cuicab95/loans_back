from factory.django import DjangoModelFactory
from .models import Customer


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
