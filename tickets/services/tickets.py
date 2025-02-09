from django.utils import timezone
from tickets.settings import app_settings
from tickets.models import TicketOrder, TicketOrderStatus


def expire_unpaid_orders():
    expiry = app_settings.UNPAID_ORDER_TICKET_EXPIRY
    expiration_time = timezone.now() - timezone.timedelta(seconds=expiry)
    expired_orders = TicketOrder.objects.filter(
        status=TicketOrderStatus.PENDING, created_at__lt=expiration_time
    )
    updated_count = expired_orders.update(status=TicketOrderStatus.CANCELLED)
    return updated_count
