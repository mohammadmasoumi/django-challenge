import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def release_expired_orders_periodic_task():
    """
    Cancels pending TicketOrders that were created more than 10 minutes ago.
    """
    from tickets.services import expire_unpaid_orders

    count = expire_unpaid_orders()
    logger.info(f"Cancelled {count} expired orders.")

    return count
