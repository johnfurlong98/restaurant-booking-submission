from django.urls import path
from .views import (
    home, 
    BookingListView, 
    BookingDetailView, 
    BookingCreateView, 
    BookingUpdateView, 
    BookingDeleteView,
)

urlpatterns = [
    path('', home, name='home'),
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/update/<int:pk>/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/delete/<int:pk>/', BookingDeleteView.as_view(), name='booking_delete'),
]
