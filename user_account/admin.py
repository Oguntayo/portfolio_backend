from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class CustomUserAdmin(UserAdmin):
    """Customize how User model appears in Django Admin"""
    model = User
    list_display = ("email", "is_staff", "is_superuser", "date_joined")
    list_filter = ("is_staff", "is_superuser", "is_active")
    ordering = ("email",)
    search_fields = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    """Customize how Profile model appears in Django Admin"""
    list_display = ("user", "bio", "website", "twitter")
    search_fields = ("user__email",)

admin.site.register(Profile, ProfileAdmin)
