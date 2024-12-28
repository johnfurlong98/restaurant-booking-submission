# reservations/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RestaurantSettings(models.Model):
    """
    A single row (typically) storing global restaurant settings,
    like working hours (open_time, close_time).
    """
    open_time = models.TimeField(
        help_text="HH:MM format for when the restaurant opens"
    )
    close_time = models.TimeField(
        help_text="HH:MM format for when the restaurant closes"
    )

    def __str__(self):
        return f"Restaurant Settings (Open: {self.open_time}, Close: {self.close_time})"


class Table(models.Model):
    """
    A model representing a physical table in the restaurant.

    name: e.g., "Table #1"
    capacity: how many guests it can seat
    table_type: optional descriptor, e.g., "window seat," "booth," etc.
    """
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    table_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        type_str = self.table_type or "N/A"
        return f"{self.name} (Capacity: {self.capacity}, Type: {type_str})"


class Booking(models.Model):
    """
    Booking can be made by a logged-in user or an anonymous user (if user is null).
    Fields:
      - user: optional link to a Django user
      - name, email, phone: contact details
      - reservation_date: date/time for the booking
      - number_of_guests
      - special_requests: optional notes
      - table: optional reference to a specific Table (if required)
      - created_on: auto timestamp
    """
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings'
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    reservation_date = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    table = models.ForeignKey(
        Table, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='bookings',
        help_text="Select a table (optional) if you want to specify a specific table."
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['reservation_date']

    def __str__(self):
        return f"{self.name} - {self.reservation_date} (Guests: {self.number_of_guests})"


class Review(models.Model):
    """
    A user-submitted review or testimonial.
    Only logged-in users can create these (in typical usage).
    Fields:
      - user: the User who wrote the review
      - title, content, rating
      - created_on: auto timestamp
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.user.username} (Rating: {self.rating})"
