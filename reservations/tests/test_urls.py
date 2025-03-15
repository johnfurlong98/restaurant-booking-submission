import pytest
from django.urls import reverse, resolve
from reservations import views

pytestmark = pytest.mark.django_db

class TestUrls:
    def test_reservation_create_url(self, table):
        url = reverse('create_reservation', kwargs={'table_id': table.pk})
        assert resolve(url).func.view_class == views.ReservationCreateView

    def test_reservation_list_url(self):
        url = reverse('reservation_list')
        assert resolve(url).func.view_class == views.ReservationListView

    def test_reservation_cancel_url(self, reservation):
        url = reverse('cancel_reservation', kwargs={'pk': reservation.pk})
        assert resolve(url).func.view_class == views.ReservationCancelView

    def test_url_names(self):
        """Test that all URL names are correctly configured"""
        urls = [
            'reservation_list',
            'booking_create',
            'review_list'
        ]
        for url_name in urls:
            try:
                reverse(url_name)
            except:
                pytest.fail(f"URL name '{url_name}' is not configured correctly")
