from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from tickets.models.utils import generate_random_id


class StadiumManager(models.Manager):
    CACHE_KEY = "STADIUM:{name}"

    def from_cache(self, *, name):
        """
        Cache stadium and it's seats
        :param name:
        :return:
        """
        key = self.CACHE_KEY.format(name=name)
        stadium = cache.get(key)

        if stadium is None:
            stadium = self.prefetch_related("seats").get(name=name)
            cache.set(key, stadium)

        return stadium

    def purge_cache(self, *, name):
        key = self.CACHE_KEY.format(name=name)
        cache.delete(key)

    def purge_all(self):
        names = self.all().values_list("name", flat=True)
        for name in names:
            self.purge_cache(name=name)


class Stadium(models.Model):
    """
    Represents a stadium where matches are held.
    """

    stadium_id = models.CharField(
        max_length=12, primary_key=True, default=generate_random_id
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StadiumManager()

    class Meta:
        verbose_name = _("Stadium")
        verbose_name_plural = _("Stadiums")

    def __str__(self):
        return self.name


class Seat(models.Model):
    """
    Represents a physical seat within a stadium.
    Decoupled from match so that the seating plan can be reused.
    """

    seat_id = models.CharField(
        max_length=12, primary_key=True, default=generate_random_id
    )
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)  # e.g., "A1", "B2", etc.
    section = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Seat")
        verbose_name_plural = _("Seats")
        unique_together = ("stadium", "seat_number")

    def __str__(self):
        return f"Seat {self.seat_number} in {self.stadium.name}"
