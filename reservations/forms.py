from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'reservation_date', 'number_of_guests', 'special_requests']

    def clean_reservation_date(self):
        date = self.cleaned_data['reservation_date']
        if date < timezone.now():
            raise ValidationError("Reservation date must be in the future.")
        return date

    def clean_number_of_guests(self):
        guests = self.cleaned_data['number_of_guests']
        if guests <= 0:
            raise ValidationError("Number of guests must be at least 1.")
        return guests
