from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking, Review, RestaurantSettings
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
