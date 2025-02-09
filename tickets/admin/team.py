from django.contrib import admin
from tickets.models import Team


@admin.action(description="Invalidate cache for selected teams")
def invalidate_team_cache(modeladmin, request, queryset):
    for team in queryset:
        team.__class__.objects.purge_cache(name=team.name)
    modeladmin.message_user(request, "Cache invalidated for selected teams.")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("team_id", "name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    actions = [invalidate_team_cache]

    def save_model(self, request, obj, form, change):
        """
        Override save_model to purge cache after saving a Team instance.
        """
        super().save_model(request, obj, form, change)
        obj.__class__.objects.purge_cache(name=obj.name)
