import pytest
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from reservations.models import Table, Reservation
from datetime import datetime, timedelta

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass123')

@pytest.fixture
def table():
    return Table.objects.create(
        table_number=1,
        capacity=4
    )

@pytest.fixture
def reservation(user, table):
    return Reservation.objects.create(
        user=user,
        table=table,
        party_size=2,
        reservation_date=datetime.now().date(),
        reservation_time=datetime.now().time(),
        status='confirmed'
    )

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def authenticated_client(client, user):
    client.login(username='testuser', password='testpass123')
    return client

@pytest.fixture
def request_with_session(request_factory):
    request = request_factory.get('/')
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    
    message_middleware = MessageMiddleware(lambda req: None)
    message_middleware.process_request(request)
    request._messages.used = False
    
    return request
