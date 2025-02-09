from django.core.management.base import BaseCommand
from django.utils import timezone
from tickets.models import TicketOrder, TicketOrderStatus


class Command(BaseCommand):
    help = "Cancels pending TicketOrders that are older than 10 minutes."

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timezone.timedelta(minutes=10)
        expired_orders = TicketOrder.objects.filter(
            status=TicketOrderStatus.PENDING, created_at__lt=expiration_time
        )
        count = expired_orders.count()
        expired_orders.update(status=TicketOrderStatus.CANCELLED)
        self.stdout.write(self.style.SUCCESS(f"Cancelled {count} expired orders."))
