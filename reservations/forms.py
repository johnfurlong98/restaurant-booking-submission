from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review, Table, RestaurantSettings
import re


class BookingForm(forms.ModelForm):
    """
    Enhanced booking form:
    - References RestaurantSettings to block out-of-hours reservations
    - Ensures table capacity isn't exceeded if a table is chosen
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
            "table",
        ]
        widgets = {
            "reservation_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                    "min": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                }
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
        reservation_date = self.cleaned_data["reservation_date"]
        if reservation_date < timezone.now():
            raise ValidationError(
                "Reservation date and time must be in the future."
            )

        # Check restaurant working hours if RestaurantSettings exist
        settings = RestaurantSettings.objects.first()
        if settings:
            # Compare times only if date is the same day or you allow multi-day
            open_dt = reservation_date.replace(
                hour=settings.open_time.hour,
                minute=settings.open_time.minute,
                second=0,
            )
            close_dt = reservation_date.replace(
                hour=settings.close_time.hour,
                minute=settings.close_time.minute,
                second=0,
            )
            if not (open_dt <= reservation_date < close_dt):
                raise ValidationError(
                    f"Bookings can only be made between {settings.open_time} and {settings.close_time}."
                )
        return reservation_date

    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data["number_of_guests"]
        if number_of_guests <= 0:
            raise ValidationError("Number of guests must be at least 1.")
        return number_of_guests

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        # Basic pattern: optional +, followed by 7-15 digits
        pattern = r"^\+?\d{7,15}$"
        if not re.match(pattern, phone):
            raise ValidationError(
                "Invalid phone number. Must contain 7-15 digits and may start with '+'."
            )
        return phone

    def clean(self):
        """
        Check table capacity vs. number_of_guests
        """
        cleaned_data = super().clean()
        table = cleaned_data.get("table")
        guests = cleaned_data.get("number_of_guests")

        if table and guests:
            if guests > table.capacity:
                raise ValidationError(
                    f"This table (capacity: {table.capacity}) can't accommodate {guests} guests."
                )
        return cleaned_data


class ReviewForm(forms.ModelForm):
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
