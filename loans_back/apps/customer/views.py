from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from loans_back.config.paginations import DefaultPagination
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from .services import LoanService


class CustomerViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["first_name", "last_name", "rfc", "curp", "contact_email", "phone_number"]
    pagination_class = DefaultPagination
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class LoanViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "customer__first_name", "customer__last_name",
        "customer__rfc", "customer__curp",
        "customer__contact_email",
        "customer__phone_number"
    ]
    pagination_class = DefaultPagination
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    service = LoanService

    def perform_create(self, serializer):
        total_amount = self.service.total_amount_with_interest_rate(
            serializer.validated_data.get('amount'),
            serializer.validated_data.get('interest_rate'),
        )
        serializer.save(total_amount=total_amount, adviser=self.request.user)
        self.service.create_loan_payments(serializer.instance)

    def perform_update(self, serializer):
        loan = serializer.instance
        change_loan_payments = self.service.validate_loan_payments(loan, serializer.validated_data)
        total_amount = self.service.total_amount_with_interest_rate(
            serializer.validated_data.get('amount'),
            serializer.validated_data.get('interest_rate'),
        ) if change_loan_payments else loan.total_amount
        serializer.save(total_amount=total_amount)
        if change_loan_payments:
            self.service.create_loan_payments(serializer.instance)

