# tickets/management/commands/seed_data.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tickets.models import Team, Stadium, Seat, Match, Ticket, TicketStatus
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample data for stadium, seats, match, tickets, and users"

    def handle(self, *args, **options):
        # ---------------------------
        # Create Teams
        # ---------------------------
        team_alpha, created = Team.objects.get_or_create(name="Alpha", code="ALP")
        self.stdout.write(self.style.SUCCESS(f"Team Alpha: {team_alpha}"))

        team_beta, created = Team.objects.get_or_create(name="Beta", code="BET")
        self.stdout.write(self.style.SUCCESS(f"Team Beta: {team_beta}"))

        # ---------------------------
        # Create a Stadium
        # ---------------------------
        stadium, created = Stadium.objects.get_or_create(
            name="National Stadium",
            defaults={
                "location": "Tehran",
                "capacity": 50000,
            },
        )
        self.stdout.write(self.style.SUCCESS(f"Stadium: {stadium}"))

        # ---------------------------
        # Create Seats for the Stadium if not exist.
        # ---------------------------
        if not stadium.seats.exists():
            # For example, rows A to J and columns 1 to 20 (total 200 seats)
            rows = [chr(i) for i in range(65, 75)]  # 'A' to 'J'
            for row in rows:
                for number in range(1, 21):
                    seat_number = f"{row}{number}"
                    Seat.objects.create(
                        stadium=stadium, seat_number=seat_number, section="Standard"
                    )
            self.stdout.write(self.style.SUCCESS("Created seats for the stadium."))
        else:
            self.stdout.write("Seats already exist for the stadium.")

        # ---------------------------
        # Create a Match at the Stadium
        # ---------------------------
        match, created = Match.objects.get_or_create(
            stadium=stadium,
            team_host=team_alpha,
            team_guest=team_beta,
            defaults={"match_date": timezone.now() + timezone.timedelta(days=7)},
        )
        self.stdout.write(self.style.SUCCESS(f"Match: {match}"))

        # ---------------------------
        # Generate Tickets for the Match if not exist.
        # ---------------------------
        if not match.tickets.exists():
            seats = stadium.seats.all()
            tickets = []
            for seat in seats:
                ticket = Ticket(
                    match=match,
                    seat=seat,
                    price=round(
                        random.uniform(50, 150), 2
                    ),  # Random price between 50 and 150
                    status=TicketStatus.AVAILABLE,
                )
                tickets.append(ticket)
            Ticket.objects.bulk_create(tickets)
            self.stdout.write(self.style.SUCCESS("Generated tickets for the match."))
        else:
            self.stdout.write("Tickets already generated for the match.")

        # ---------------------------
        # Create some Users if they do not exist.
        # ---------------------------
        if User.objects.count() < 5:
            for i in range(1, 6):
                phone_number = f"+9891234567{i:02d}"
                if not User.objects.filter(phone_number=phone_number).exists():
                    user = User.objects.create_user(
                        phone_number=phone_number, password="password123"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Created user: {user.phone_number}")
                    )
        else:
            self.stdout.write("Users already exist.")

        self.stdout.write(self.style.SUCCESS("Seed data generation complete."))
