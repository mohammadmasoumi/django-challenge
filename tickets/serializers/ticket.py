from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from tickets.serializers import MatchSerializer, SeatSerializer
from tickets.models import Ticket, TicketOrder, TicketStatus


class TicketSerializer(serializers.ModelSerializer):
    # Writeable fields for input (primary keys)
    match = serializers.PrimaryKeyRelatedField(
        queryset=Ticket._meta.get_field("match").remote_field.model.objects.all()
    )
    seat = serializers.PrimaryKeyRelatedField(
        queryset=Ticket._meta.get_field("seat").remote_field.model.objects.all()
    )

    # Nested read-only representations
    match_detail = MatchSerializer(source="match", read_only=True)
    seat_detail = SeatSerializer(source="seat", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "ticket_id",
            "match",
            "match_detail",
            "seat",
            "seat_detail",
            "ticket_type",
            "price",
            "status",
            "purchased_at",
            "updated_at",
        )
        read_only_fields = (
            "ticket_id",
            "status",
            "purchased_at",
            "updated_at",
        )


class TicketOrderSerializer(serializers.ModelSerializer):
    # Accept a list of ticket IDs for purchase.
    tickets = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ticket.objects.filter(status=TicketStatus.AVAILABLE),
        help_text=_("List of ticket IDs to purchase."),
    )

    class Meta:
        model = TicketOrder
        fields = (
            "order_id",
            "tickets",
            "user",
            "status",
            "payment_status",
            "total_amount",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "order_id",
            "user",
            "status",
            "payment_status",
            "total_amount",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        # Extract the list of Ticket instances (provided via their primary keys)
        tickets = validated_data.pop("tickets")
        user = self.context["request"].user

        # Gather the IDs of the tickets to purchase.
        ticket_ids = [ticket.ticket_id for ticket in tickets]

        with transaction.atomic():
            # Lock the selected tickets for update.
            locked_tickets = list(
                Ticket.objects.select_for_update().filter(ticket_id__in=ticket_ids)
            )

            # Validate that we have locked all the tickets requested.
            if len(locked_tickets) != len(ticket_ids):
                raise serializers.ValidationError(
                    "One or more selected tickets are not available."
                )

            # Validate that each locked ticket is still available.
            for ticket in locked_tickets:
                if ticket.status != TicketStatus.AVAILABLE:
                    raise serializers.ValidationError(
                        f"Ticket {ticket.ticket_id} is not available."
                    )

            # Calculate the total amount from the locked tickets.
            total_amount = sum(ticket.price for ticket in locked_tickets)

            # Create the TicketOrder.
            order = TicketOrder.objects.create(user=user, total_amount=total_amount)

            now = timezone.now()
            # Update each ticket to assign it to the order, mark it as sold, and record the purchase time.
            for ticket in locked_tickets:
                ticket.order = order
                ticket.status = TicketStatus.SOLD
                ticket.purchased_at = now
                ticket.save()

        return order
