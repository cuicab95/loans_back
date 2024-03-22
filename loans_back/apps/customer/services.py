from datetime import date
from dateutil.relativedelta import relativedelta
from .catalogs import PaymentIntervalChoices
from .models import LoanPayments


class LoanService:

    @classmethod
    def total_amount_with_interest_rate(cls, amount, interest_rate):
        total = amount + (amount * (interest_rate/100))
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
