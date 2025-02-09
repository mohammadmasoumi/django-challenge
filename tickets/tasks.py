import logging

from celery import shared_task
from django.utils import timezone
from tickets.models import TicketOrder, TicketOrderStatus

logger = logging.getLogger(__name__)


@shared_task
def release_expired_orders_periodic_task():
    """
    Cancels pending TicketOrders that were created more than 10 minutes ago.
    """
    expiration_time = timezone.now() - timezone.timedelta(minutes=10)
    expired_orders = TicketOrder.objects.filter(
        status=TicketOrderStatus.PENDING, created_at__lt=expiration_time
    )
    count = expired_orders.count()
    expired_orders.update(status=TicketOrderStatus.CANCELLED)
    logger.info("Cancelled %d expired orders." % count)
    return count
