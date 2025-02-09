from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _
from tickets.services import expire_unpaid_orders


class Command(BaseCommand):
    help = _("Cancels pending TicketOrders that are older than 10 minutes.")

    def handle(self, *args, **kwargs):
        count = expire_unpaid_orders()
        self.stdout.write(self.style.SUCCESS(f"Cancelled {count} expired orders."))
