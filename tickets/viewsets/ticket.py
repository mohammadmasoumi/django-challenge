from rest_framework import viewsets
from tickets.models import TicketOrder
from tickets.serializers import TicketOrderSerializer


class TicketOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating and managing ticket orders.
    """

    serializer_class = TicketOrderSerializer
    queryset = TicketOrder.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
