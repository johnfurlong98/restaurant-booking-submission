from django.contrib import admin
from .models import Booking, Review, RestaurantSettings, Table, MenuCategory, MenuItem


@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    """
    Admin can set open_time and close_time here.
    We'll assume only one instance is typically used.
    """

    list_display = ("open_time", "close_time")


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "table_type")
    search_fields = ("name", "table_type")

    def add_view(self, request, form_url="", extra_context=None):
        """
        A custom approach if we want to allow 'batch creation' of multiple tables
        of the same type. Example snippet:
        """
        return super().add_view(request, form_url, extra_context)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "reservation_date",
        "number_of_guests",
        "table",
        "user",
    )
    list_filter = ("reservation_date", "number_of_guests", "table")
    search_fields = ("name", "email", "phone")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "rating", "created_on")
    list_filter = ("rating",)
    search_fields = ("title", "content", "user__username")


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    search_fields = ("name",)
    ordering = ["order", "name"]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_vegetarian",
        "is_vegan",
        "is_gluten_free",
        "is_available",
    )
    list_filter = (
        "category",
        "is_vegetarian",
        "is_vegan",
        "is_gluten_free",
        "is_available",
    )
    search_fields = ("name", "description")
    ordering = ["category", "name"]
