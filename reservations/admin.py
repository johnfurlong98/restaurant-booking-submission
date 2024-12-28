from django.contrib import admin
from .models import Booking, Review, RestaurantSettings, Table


@admin.register(RestaurantSettings)
class RestaurantSettingsAdmin(admin.ModelAdmin):
    """
    Admin can set open_time and close_time here.
    We'll assume only one instance is typically used.
    """
    list_display = ('open_time', 'close_time')


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'table_type')
    search_fields = ('name', 'table_type')

    def add_view(self, request, form_url='', extra_context=None):
        """
        A custom approach if we want to allow 'batch creation' of multiple tables 
        of the same type. Example snippet:
        """
        # Optionally, you can override the GET/POST flow to handle batch creation.
        return super().add_view(request, form_url, extra_context)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'reservation_date', 'number_of_guests', 'table', 'user')
    list_filter = ('reservation_date', 'number_of_guests', 'table')
    search_fields = ('name', 'email', 'phone')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'rating', 'created_on')
    list_filter = ('rating',)
    search_fields = ('title', 'content', 'user__username')
