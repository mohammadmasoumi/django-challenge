from django.contrib import admin
from tickets.models import Stadium, Seat


# Custom admin actions for cache management
def purge_stadium_cache(modeladmin, request, queryset):
    for stadium in queryset:
        Stadium.objects.purge_cache(name=stadium.name)


purge_stadium_cache.short_description = "Purge cache for selected stadiums"


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "capacity", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "location")
    readonly_fields = ("stadium_id", "created_at", "updated_at")
    actions = [purge_stadium_cache]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("stadium_id", "name", "location", "capacity")},
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("seat_number", "stadium", "section", "is_active")
    list_filter = ("stadium", "section", "is_active")
    search_fields = ("seat_number", "stadium__name")
    readonly_fields = ("seat_id", "created_at", "updated_at")

    fieldsets = (
        (
            "Seat Information",
            {"fields": ("seat_id", "stadium", "seat_number", "section")},
        ),
        ("Status", {"fields": ("is_active",)}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
