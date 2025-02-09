from rest_framework import viewsets
from tickets.models import Payment
from tickets.settings import app_settings
from tickets.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for processing payments for ticket orders.
    When a payment is created and marked completed, the associated order is finalized.
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = app_settings.DEFAULT_PERMISSION_CLASSES
    authentication_classes = app_settings.DEFAULT_AUTHENTICATION_CLASSES

    def get_queryset(self):
        return self.queryset.filter(ticket_order__user=self.request.user)
