from django.db import models


class GenderChoices(models.TextChoices):
    women = "women", "Mujer"
    man = "man", "Hombre"


class LoadKindChoices(models.TextChoices):
    vacations = "vacations", "Vacaciones"
    business_improvements = "business_improvements", "Mejoras de negocios"
    debt_payment = "debt_payment", "Pago de deuda"
    education = "education", "Educación"
    event = "event", "Eventos"
    other = "other", "Otro"


class PaymentIntervalChoices(models.TextChoices):
    month = "month", "Meses"
    year = "year", "Años"


class PaymentStatusChoices(models.TextChoices):
    paid = "paid", "Pagado"
    pending = "pending", "Pendiente"

