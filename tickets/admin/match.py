from django.contrib import admin
from tickets.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "match_id",
        "stadium",
        "match_date",
        "team_host",
        "team_guest",
        "created_at",
        "updated_at",
    )
    search_fields = ("match_id", "stadium__name", "team_host__name", "team_guest__name")
    list_filter = ("match_date", "stadium")
