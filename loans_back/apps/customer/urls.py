from django.urls import path
from rest_framework import routers
from . import views

app_name = "customer"
router = routers.SimpleRouter()
router.register("customer", views.CustomerViewSet)
urlpatterns = router.urls
