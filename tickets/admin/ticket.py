from django.contrib import admin
from tickets.models import TicketOrder, Ticket, Payment, Team


class TicketInline(admin.TabularInline):
    """
    Inline admin interface for Ticket model within TicketOrder.
    Shows ticket details (read-only) to help review the order’s tickets.
    """

    model = Ticket
    extra = 0
    readonly_fields = (
        "ticket_id",
        "match",
        "seat",
        "ticket_type",
        "price",
        "status",
        "purchased_at",
        "updated_at",
    )
    can_delete = False


@admin.register(TicketOrder)
class TicketOrderAdmin(admin.ModelAdmin):
    """
    Admin view for TicketOrder.
    Displays key fields and includes an inline view of associated tickets.
    """

    list_display = (
        "order_id",
        "user",
        "total_amount",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("order_id", "user__username", "user__email")
    inlines = [TicketInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Admin view for Ticket.
    Displays information about each ticket.
    """

    list_display = (
        "ticket_id",
        "order",
        "match",
        "seat",
        "ticket_type",
        "price",
        "status",
        "purchased_at",
    )
    list_filter = ("ticket_type", "status", "purchased_at")
    search_fields = ("ticket_id", "order__order_id")
