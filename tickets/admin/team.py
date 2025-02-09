from django.contrib import admin
from tickets.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """
    Admin view for Team.
    Displays team details and allows searching by name or code.
    """

    list_display = ("team_id", "name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
