import uuid
from django.core.cache import cache
from django.db import models


class MatchManager(models.Manager):
    CACHE_KEY = "MATCH:{name}"

    def from_cache(self, *, name):
        """
        Cache matches by name
        :param name:
        :return:
        """
        key = self.CACHE_KEY.format(name=name)
        team = cache.get(key)

        if team is None:
            team = self.get(name=name)
            cache.set(key, team)

        return team

    def purge_cache(self, *, name):
        key = self.CACHE_KEY.format(name=name)
        cache.delete(key)

    def purge_all(self):
        names = self.all().values_list("name", flat=True)
        for name in names:
            self.purge_cache(name=name)


class Match(models.Model):
    """
    Represents a volleyball match scheduled at a stadium.
    """

    match_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    stadium = models.ForeignKey(
        "Stadium", on_delete=models.CASCADE, related_name="matches"
    )
    match_date = models.DateTimeField()
    team_host = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="matches_as_host"
    )
    team_guest = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="matches_as_guest"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MatchManager()

    def __str__(self):
        return f"{self.team_host} vs {self.team_guest} at {self.stadium.name}"
