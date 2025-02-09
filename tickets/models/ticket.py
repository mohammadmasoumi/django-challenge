import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TicketOrderStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    CONFIRMED = "confirmed", _("Confirmed")
    CANCELLED = "cancelled", _("Cancelled")


class TicketOrder(models.Model):
    """
    Represents a purchase order for one or more tickets.
    An order is created in a pending state and must be paid within 10 minutes.
    """

    order_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ticket_orders"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=TicketOrderStatus.choices,
        default=TicketOrderStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        """
        Returns True if the order has been pending for more than 10 minutes.
        """
        expiration_time = timezone.now() - timezone.timedelta(minutes=10)
        return (
            self.created_at < expiration_time
            and self.status == TicketOrderStatus.PENDING
        )

    def __str__(self):
        return f"Order #{self.pk} by {self.user} ({self.status})"


class TicketStatus(models.TextChoices):
    ACTIVE = "active", _("Active")
    USED = "used", _("Used")
    CANCELLED = "cancelled", _("Cancelled")


class TicketTypeStatus(models.TextChoices):
    REGULAR = "regular", _("Regular")
    VIP = "vip", _("VIP")
    PREMIUM = "premium", _("Premium")


class Ticket(models.Model):
    """
    Represents an individual ticket that assigns a specific seat to a match.
    The unique_together constraint prevents double booking the same seat for a match.
    """

    ticket_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    order = models.ForeignKey(
        TicketOrder, on_delete=models.CASCADE, related_name="tickets"
    )
    match = models.ForeignKey("Match", on_delete=models.CASCADE, related_name="tickets")
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, related_name="tickets")
    ticket_type = models.CharField(
        max_length=50,
        choices=TicketTypeStatus.choices,
        default=TicketTypeStatus.REGULAR,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=TicketStatus.choices, default=TicketStatus.ACTIVE
    )
    purchased_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("match", "seat")

    def __str__(self):
        return f"Ticket {self.pk} for {self.match} - Seat {self.seat}"
