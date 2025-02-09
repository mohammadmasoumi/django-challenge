from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from tickets.models import Stadium, Seat


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = (
        "seat_id",
        "seat_number",
        "section",
        "is_active",
        "created_at",
        "updated_at",
    )
    can_delete = False


@admin.action(description=_("Invalidate cache for selected stadiums"))
def invalidate_stadium_cache(modeladmin, request, queryset):
    for stadium in queryset:
        stadium.__class__.objects.purge_cache(name=stadium.name)
    modeladmin.message_user(request, _("Cache invalidated for selected stadiums."))


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = (
        "stadium_id",
        "name",
        "location",
        "capacity",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("stadium_id", "name", "location")
    list_filter = ("is_active",)
    inlines = [SeatInline]
    actions = [invalidate_stadium_cache]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Purge cache on save
        obj.__class__.objects.purge_cache(name=obj.name)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "seat_id",
        "stadium",
        "seat_number",
        "section",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("seat_id", "seat_number", "section", "stadium__name")
    list_filter = ("is_active", "stadium")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Purge the stadium cache when a seat is updated.
        obj.stadium.__class__.objects.purge_cache(name=obj.stadium.name)
