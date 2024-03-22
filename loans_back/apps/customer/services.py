from datetime import date
from dateutil.relativedelta import relativedelta
from .catalogs import PaymentIntervalChoices, PaymentStatusChoices
from .models import LoanPayments
from rest_framework.exceptions import ValidationError
from .messages import ERROR_LOAN_PAYMENT_PAID


class LoanService:

    @classmethod
    def total_amount_with_interest_rate(cls, amount, interest_rate):
        total = round(amount + (amount * (interest_rate/100)),2)
        return total

    @classmethod
    def create_loan_payments(cls, loan):
        today = date.today()
        i = 1
        start_date = today
        amount = loan.total_amount / loan.payment_duration
        while i <= loan.payment_duration:
            if loan.payment_interval == PaymentIntervalChoices.month:
                start_date += relativedelta(months=1)
                end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
            else:
                start_date += relativedelta(years=1)
                end_date = start_date + relativedelta(years=1) - relativedelta(days=1)
            LoanPayments.objects.create(
                loan=loan,
                start_date=start_date,
                end_date=end_date,
                amount=round(amount, 2),
            )
            i += 1

    @classmethod
    def validate_loan_payments(cls, loan, validated_data):
        updated_payment_duration = loan.payment_duration != validated_data.get('payment_duration')
        updated_payment_interval = loan.payment_interval != validated_data.get('payment_interval')
        updated_amount = loan.amount != validated_data.get('amount')
        updated_interest_rate = loan.interest_rate != validated_data.get('interest_rate')
        if updated_payment_duration or updated_payment_interval or updated_amount or updated_interest_rate:
            if loan.payments.filter(status=PaymentStatusChoices.paid).exists():
                raise ValidationError(ERROR_LOAN_PAYMENT_PAID)
            loan.payments.all().delete()
            return True
        return False
