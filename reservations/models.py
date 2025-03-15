# reservations/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError


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
    table_number = models.IntegerField(default=1)
    capacity = models.IntegerField(default=4)

    def __str__(self):
        return f'Table {self.table_number} (Capacity: {self.capacity})'

    def is_available(self, date, time):
        if isinstance(time, str):
            time = datetime.strptime(time, '%H:%M').time()
        return not Reservation.objects.filter(
            table=self,
            reservation_date=date,
            reservation_time=time,
            status='confirmed'
        ).exists()


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    party_size = models.IntegerField()
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Reservation for {self.user.username} at Table {self.table.table_number}'

    def clean(self):
        # Skip validation if the reservation is being cancelled
        if self.status == 'cancelled':
            return

        if self.party_size and self.table and self.party_size > self.table.capacity:
            raise ValidationError('Party size cannot exceed table capacity')

        if self.table and self.reservation_date and self.reservation_time:
            if not self.table.is_available(self.reservation_date, self.reservation_time):
                raise ValidationError('Table is not available at this time')

        if self.reservation_date and self.reservation_date < timezone.now().date():
            raise ValidationError('Cannot make reservations for past dates')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Booking(models.Model):
    """
    Booking can be made by a logged-in user or an anonymous user (if user is null).
    Fields:
      - user: optional link to a Django user
      - name, email, phone: contact details
      - reservation_date: date/time for the booking
      - number_of_guests
      - special_requests: optional notes
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
