from django.contrib import admin
from .models import (
    RestaurantSettings,
    Booking,
    Review,
)


@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    """
    Admin can set open_time and close_time here.
    We'll assume only one instance is typically used.
    """
    list_display = ("open_time", "close_time")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "reservation_date",
        "number_of_guests",
    )
    list_filter = ("reservation_date", "number_of_guests")
    search_fields = ("name", "email", "phone")
    date_hierarchy = "reservation_date"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "rating", "created_on")
    list_filter = ("rating", "created_on")
    search_fields = ("title", "content", "user__username")
    date_hierarchy = "created_on"
