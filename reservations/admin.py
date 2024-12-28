from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'reservation_date', 'number_of_guests')
    list_filter = ('reservation_date', 'number_of_guests')
    search_fields = ('name', 'email', 'phone')
