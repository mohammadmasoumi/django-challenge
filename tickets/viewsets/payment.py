from rest_framework import viewsets
from tickets.models import Payment
from tickets.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for processing payments for ticket orders.
    When a payment is created and marked completed, the associated order is finalized.
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        return self.queryset.filter(ticket_order__user=self.request.user)
