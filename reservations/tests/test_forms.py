import pytest
from django.utils import timezone
from reservations.forms import ReservationForm
from datetime import datetime, timedelta

pytestmark = pytest.mark.django_db

class TestReservationForm:
    def test_valid_reservation_form(self, table):
        form_data = {
            'party_size': 2,
            'reservation_date': (timezone.now() + timedelta(days=1)).date(),
            'reservation_time': '12:00'
        }
        form = ReservationForm(data=form_data, table=table)
        assert form.is_valid()

    def test_invalid_party_size(self, table):
        form_data = {
            'party_size': 10,  # Greater than table capacity
            'reservation_date': (timezone.now() + timedelta(days=1)).date(),
            'reservation_time': '12:00'
        }
        form = ReservationForm(data=form_data, table=table)
        assert not form.is_valid()
        assert 'party_size' in form.errors

    def test_past_date_reservation(self, table):
        form_data = {
            'party_size': 2,
            'reservation_date': (timezone.now() - timedelta(days=1)).date(),
            'reservation_time': '12:00'
        }
        form = ReservationForm(data=form_data, table=table)
        assert not form.is_valid()
        assert 'reservation_date' in form.errors
