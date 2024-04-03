from rest_framework import routers
from . import views

app_name = "customer"
router = routers.SimpleRouter()
router.register("customer", views.CustomerViewSet)
router.register("loan", views.LoanViewSet)
router.register("refund", views.RefundPaymentViewSet)
urlpatterns = router.urls
