from rest_framework import serializers
from .models import Customer


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
