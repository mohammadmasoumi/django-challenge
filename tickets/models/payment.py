from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentStatus(models.TextChoices):
    PENDING = (
        "pending",
        _("Pending"),
    )
    COMPLETED = (
        "completed",
        _("Completed"),
    )
    FAILED = (
        "failed",
        _("Failed"),
    )


class Payment(models.Model):
    """
    Represents a payment for a TicketOrder.
    Once a payment is processed successfully, the order is finalized.
    """

    # One-to-one relationship ensures an order can have only one payment.
    ticket_order = models.OneToOneField(
        "TicketOrder", on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)  # e.g., 'credit_card', 'paypal'
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.ticket_order} - {self.status}"
