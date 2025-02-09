from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tickets.viewsets import TicketOrderViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"orders", TicketOrderViewSet, basename="orders")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
]
