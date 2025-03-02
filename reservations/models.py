# reservations/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


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

    def is_available(self, check_date, duration_minutes=120):
        """
        Check if the table is available at the given date/time.
        By default, checks for 2-hour window around the requested time.
        """
        # Convert check_date to UTC if it's not already
        if timezone.is_naive(check_date):
            check_date = timezone.make_aware(check_date)
        
        # Define the time window
        start_time = check_date - timedelta(minutes=duration_minutes/2)
        end_time = check_date + timedelta(minutes=duration_minutes/2)
        
        # Check for overlapping bookings
        overlapping_bookings = self.bookings.filter(
            reservation_date__gt=start_time,
            reservation_date__lt=end_time
        ).exists()
        
        return not overlapping_bookings

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
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    reservation_date = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    table = models.ForeignKey(
        Table,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
        help_text="Select a table (optional) if you want to specify a specific table.",
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["reservation_date"]

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
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} by {self.user.username} (Rating: {self.rating})"


class MenuCategory(models.Model):
    """
    Categories for menu items (e.g., Starters, Main Course, Desserts)
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Menu Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Individual menu items with prices and descriptions
    """
    category = models.ForeignKey(MenuCategory, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} (£{self.price})"
