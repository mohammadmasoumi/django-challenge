from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tickets.viewsets import TicketViewSet, TicketOrderViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"tickets", TicketViewSet, basename="tickets")
router.register(r"orders", TicketOrderViewSet, basename="ticket-orders")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", include(router.urls)),
]
