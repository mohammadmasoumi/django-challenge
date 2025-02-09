# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for our extended User model.
    Uses phone_number as the primary identifier and excludes username.
    """

    list_display = (
        "phone_number",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    search_fields = ("phone_number", "first_name", "last_name", "email")
    ordering = ("phone_number",)

    # Use custom fieldsets to only display fields relevant to our model.
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # When adding a new user, display these fields.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "email",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
