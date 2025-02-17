from django.contrib import admin

from api.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["email", "first_name", "last_name"]
