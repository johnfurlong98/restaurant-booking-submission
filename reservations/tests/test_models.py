import pytest
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from reservations.models import Table, Reservation

pytestmark = pytest.mark.django_db

class TestTableModel:
    def test_table_creation(self, table):
        assert table.table_number == 1
        assert table.capacity == 4
        assert str(table) == f'Table {table.table_number} (Capacity: {table.capacity})'

    def test_table_availability(self, table, reservation):
        # Test table availability for a specific time
        date = datetime.now().date()
        time = datetime.strptime('12:00', '%H:%M').time()
        
        # Update the reservation to match the test time
        reservation.reservation_date = date
        reservation.reservation_time = time
        reservation.save()
        
        assert not table.is_available(date, time)
        
        # Test availability for a different time
        different_time = datetime.strptime('15:00', '%H:%M').time()
        assert table.is_available(date, different_time)

class TestReservationModel:
    def test_reservation_creation(self, reservation, user, table):
        assert reservation.user == user
        assert reservation.table == table
        assert reservation.party_size == 2
        assert reservation.status == 'confirmed'
        assert str(reservation) == f'Reservation for {user.username} at Table {table.table_number}'

    def test_invalid_party_size(self, user, table):
        with pytest.raises(ValidationError):
            Reservation.objects.create(
                user=user,
                table=table,
                party_size=10,  # Greater than table capacity
                reservation_date=datetime.now().date(),
                reservation_time='12:00',
                status='confirmed'
            )

    def test_duplicate_reservation_time(self, user, table, reservation):
        # Try to create a reservation for the same table at the same time
        with pytest.raises(ValidationError):
            Reservation.objects.create(
                user=user,
                table=table,
                party_size=2,
                reservation_date=reservation.reservation_date,
                reservation_time=reservation.reservation_time,
                status='confirmed'
            )
