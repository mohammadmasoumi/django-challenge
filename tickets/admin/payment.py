from django.contrib import admin
from tickets.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin view for Payment.
    Displays key details about a payment, including its associated order.
    """

    list_display = (
        "ticket_order",
        "amount",
        "payment_method",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("ticket_order__order_id",)
