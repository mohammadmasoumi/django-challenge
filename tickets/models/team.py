from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from tickets.models.utils import generate_random_id


class TeamManager(models.Manager):
    CACHE_KEY = "TEAM:{name}"

    def from_cache(self, *, name):
        """
        Cache team
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


class Team(models.Model):
    team_id = models.CharField(
        max_length=12, primary_key=True, default=generate_random_id
    )
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TeamManager()

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    def __str__(self):
        return self.code
