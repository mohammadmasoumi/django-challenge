from rest_framework import viewsets, filters
from tickets.models import Ticket, TicketOrder
from tickets.settings import app_settings
from tickets.serializers import TicketSerializer, TicketOrderSerializer


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving tickets.
    Typically used to show available tickets and ticket details.
    """

    queryset = Ticket.objects.prefetch_related(
        "match",
        "match__team_host",
        "match__team_guest",
        "match__stadium",
        "seat",
        "seat__stadium",
    ).all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["ticket_id", "match__match_id", "seat__seat_number"]
    ordering_fields = ["price", "purchased_at"]
    permission_classes = app_settings.DEFAULT_PERMISSION_CLASSES
    authentication_classes = app_settings.DEFAULT_AUTHENTICATION_CLASSES


class TicketOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating and managing ticket orders.
    Users can create an order by submitting a list of ticket IDs.
    """

    serializer_class = TicketOrderSerializer
    queryset = TicketOrder.objects.all()
    permission_classes = app_settings.DEFAULT_PERMISSION_CLASSES
    authentication_classes = app_settings.DEFAULT_AUTHENTICATION_CLASSES

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
