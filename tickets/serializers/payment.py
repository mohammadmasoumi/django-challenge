from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from tickets.models import TicketOrder, TicketOrderStatus, Payment, PaymentStatus

EXPIRATION_TIME_SECONDS = 600


class PaymentSerializer(serializers.ModelSerializer):
    # Allow only orders that are still pending.
    ticket_order_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketOrder.objects.filter(status="pending"), source="ticket_order"
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "ticket_order_id",
            "amount",
            "payment_method",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "status", "created_at", "updated_at")

    def validate(self, data):
        ticket_order = data["ticket_order"]
        # Ensure the order is pending
        if ticket_order.status != "pending":
            raise serializers.ValidationError(_("Ticket order is not pending payment."))
        # Ensure the order is not expired (10 minutes)
        if (
            timezone.now() - ticket_order.created_at
        ).total_seconds() > EXPIRATION_TIME_SECONDS:
            raise serializers.ValidationError(
                _("Ticket order has expired. Please create a new order.")
            )
        # Payment amount must match the order total.
        if data["amount"] != ticket_order.total_amount:
            raise serializers.ValidationError(
                _("Payment amount does not match the order total.")
            )
        return data

    def create(self, validated_data):
        from django.db import transaction

        ticket_order = validated_data["ticket_order"]
        with transaction.atomic():
            # Simulate payment processing (in production, integrate with a real payment gateway)
            payment = Payment.objects.create(
                **validated_data, status=PaymentStatus.COMPLETED
            )
            ticket_order.status = TicketOrderStatus.CONFIRMED
            ticket_order.save()
        return payment
