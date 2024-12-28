from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Booking, Review

class BookingModelTest(TestCase):
    def test_booking_str(self):
        booking = Booking.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='123456',
            reservation_date=timezone.now() + timedelta(days=1),
            number_of_guests=2
        )
        self.assertIn("John Doe", str(booking))

class BookingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_booking_create_view(self):
        # Test booking form access
        response = self.client.get(reverse('booking_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/booking_create.html')
