import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from reservations.models import Reservation

pytestmark = pytest.mark.django_db

class TestReservationViews:
    def test_reservation_create_view(self, authenticated_client, table):
        url = reverse('create_reservation', kwargs={'table_id': table.pk})
        response = authenticated_client.get(url)
        assert response.status_code == 200

        data = {
            'table': table.id,
            'party_size': 2,
            'reservation_date': (timezone.now() + timedelta(days=1)).date(),
            'reservation_time': '14:00',
            'special_requests': 'None'
        }
        response = authenticated_client.post(url, data)
        assert response.status_code == 302  # Redirect after successful creation
        assert Reservation.objects.filter(table=table).exists()

    def test_reservation_list_view(self, authenticated_client, reservation):
        url = reverse('reservation_list')
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert reservation in response.context['reservations']

    def test_reservation_cancel_view(self, authenticated_client, reservation):
        url = reverse('cancel_reservation', kwargs={'pk': reservation.pk})
        response = authenticated_client.post(url)
        assert response.status_code == 302
        
        # Refresh reservation from database
        reservation.refresh_from_db()
        assert reservation.status == 'cancelled'

    def test_unauthorized_reservation_access(self, client, reservation):
        # Test that unauthenticated users cannot access reservation views
        url = reverse('reservation_list')
        response = client.get(url)
        assert response.status_code == 302  # Redirect to login
        assert '/login/' in response.url
