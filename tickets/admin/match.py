from django.contrib import admin
from django.utils.html import format_html
from tickets.models import Match


def purge_match_cache(modeladmin, request, queryset):
    for match in queryset:
        # You might want to implement a cache key strategy for matches
        pass


purge_match_cache.short_description = "Purge cache for selected matches"


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("match_date", "team_host", "team_guest", "stadium", "status")
    list_filter = ("stadium", "match_date")
    search_fields = ("team_host__name", "team_guest__name", "stadium__name")
    readonly_fields = ("match_id", "created_at", "updated_at", "match_preview")
    actions = [purge_match_cache]

    fieldsets = (
        (
            "Match Information",
            {
                "fields": (
                    "match_id",
                    "stadium",
                    "match_date",
                    "team_host",
                    "team_guest",
                )
            },
        ),
        (
            "Status & Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
        ("Preview", {"fields": ("match_preview",), "classes": ("collapse",)}),
    )

    def match_preview(self, obj):
        return format_html(
            f"<strong>{obj.team_host} vs {obj.team_guest}</strong><br>"
            f"Date: {obj.match_date}<br>"
            f"Location: {obj.stadium.name}"
        )

    match_preview.short_description = "Preview"

    def status(self, obj):
        from django.utils.timezone import now

        if obj.match_date > now():
            return format_html('<span style="color: green;">Upcoming</span>')
        return format_html('<span style="color: gray;">Completed</span>')

    status.short_description = "Status"
