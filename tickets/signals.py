from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Stadium, Seat, Team


@receiver(post_save, sender=Stadium)
def invalidate_stadium_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate the cache for a stadium when it is saved.
    """
    sender.objects.purge_cache(name=instance.name)


@receiver(post_delete, sender=Stadium)
def invalidate_stadium_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the cache for a stadium when it is deleted.
    """
    sender.objects.purge_cache(name=instance.name)


@receiver(post_save, sender=Seat)
def invalidate_stadium_cache_on_seat_save(sender, instance, **kwargs):
    """
    Invalidate the stadium cache whenever a seat is added or updated,
    since the stadium is cached along with its seats.
    """
    Stadium.objects.purge_cache(name=instance.stadium.name)


@receiver(post_delete, sender=Seat)
def invalidate_stadium_cache_on_seat_delete(sender, instance, **kwargs):
    """
    Invalidate the stadium cache when a seat is deleted.
    """
    Stadium.objects.purge_cache(name=instance.stadium.name)


@receiver(post_save, sender=Team)
def invalidate_team_cache_on_save(sender, instance, **kwargs):
    """
    Purge the cache for a Team when it is saved.
    """
    sender.objects.purge_cache(name=instance.name)


@receiver(post_delete, sender=Team)
def invalidate_team_cache_on_delete(sender, instance, **kwargs):
    """
    Purge the cache for a Team when it is deleted.
    """
    sender.objects.purge_cache(name=instance.name)
