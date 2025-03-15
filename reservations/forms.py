from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review, Reservation, Table
import re


class BaseForm(forms.ModelForm):
    """
    Base form class with common validation methods
    """
    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        if phone:
            pattern = r"^\+?\d{7,15}$"
            if not re.match(pattern, phone):
                raise ValidationError(
                    "Invalid phone number. Must contain 7-15 digits and may start with '+'."
                )
        return phone


class BookingForm(BaseForm):
    """
    Enhanced booking form:
    - References RestaurantSettings to block out-of-hours reservations
    """

    class Meta:
        model = Booking
        fields = [
            "name",
            "email",
            "phone",
            "reservation_date",
            "number_of_guests",
            "special_requests",
        ]
        widgets = {
            "reservation_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "number_of_guests": forms.NumberInput(
                attrs={"class": "form-control"}
            ),
            "special_requests": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def clean_reservation_date(self):
        """
        Check that the reservation date is in the future.
        """
        reservation_date = self.cleaned_data["reservation_date"]
        if reservation_date < timezone.now():
            raise forms.ValidationError("Please select a future date and time.")
        return reservation_date

    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data["number_of_guests"]
        if number_of_guests <= 0:
            raise ValidationError("Number of guests must be at least 1.")
        return number_of_guests


class ReviewForm(BaseForm):
    """
    For user reviews
    """

    class Meta:
        model = Review
        fields = ["title", "content", "rating"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return rating


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['party_size', 'reservation_date', 'reservation_time']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
            'reservation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.table = kwargs.pop('table', None)
        super().__init__(*args, **kwargs)
        if self.table:
            self.instance.table = self.table

    def clean(self):
        cleaned_data = super().clean()
        party_size = cleaned_data.get('party_size')
        reservation_date = cleaned_data.get('reservation_date')
        reservation_time = cleaned_data.get('reservation_time')

        if not self.table:
            raise ValidationError('Table is required')

        if party_size and party_size > self.table.capacity:
            self.add_error('party_size', 'Party size cannot exceed table capacity')

        if reservation_date and reservation_date < timezone.now().date():
            self.add_error('reservation_date', 'Cannot make reservations for past dates')

        if self.table and reservation_date and reservation_time:
            if not self.table.is_available(reservation_date, reservation_time):
                self.add_error('reservation_time', 'Table is not available at this time')

        return cleaned_data
