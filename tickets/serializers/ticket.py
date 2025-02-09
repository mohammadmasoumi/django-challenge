from django.db import transaction, IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from tickets.models import TicketOrder, Ticket, TicketOrderStatus


class TicketSerializer(serializers.ModelSerializer):
    match_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), source="match"
    )
    seat_id = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(), source="seat"
    )

    class Meta:
        model = Ticket
        fields = ("match_id", "seat_id", "ticket_type", "price")


class TicketOrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = TicketOrder
        fields = ("order_id", "user", "created_at", "total_amount", "status", "tickets")
        read_only_fields = ("order_id", "created_at", "status", "total_amount", "user")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        user = self.context["request"].user
        total_amount = sum([ticket["price"] for ticket in tickets_data])
        order = TicketOrder.objects.create(
            user=user,
            total_amount=total_amount,
            status=TicketOrderStatus.PENDING,
            **validated_data,
        )

        # Prepare ticket instances for bulk creation.
        ticket_instances = [
            Ticket(order=order, **ticket_data) for ticket_data in tickets_data
        ]
        try:
            with transaction.atomic():
                # Pros and Cons
                # 1. Signals and Custom Save Logic:
                #   Django’s bulk_create bypasses the model’s save() method and does not trigger model signals.
                # 2. Error Handling:
                #   If one of the ticket records violates a database constraint (like the unique constraint on
                #       match and seat), the entire bulk operation will fail.
                # 3. Validation:
                #   While your serializer validation will catch many issues upfront, batch processing means that if
                #       one ticket fails at the database level, you have to roll back the entire transaction.
                # 4. Scalability:
                #   Using batch processing reduces the load on your database and improves throughput, which
                #       is particularly valuable in a high-concurrency ticketing system.
                Ticket.objects.bulk_create(ticket_instances)
        except IntegrityError:
            raise serializers.ValidationError(
                _("One or more selected seats are already booked for this match.")
            )
        return order
