from django.urls import path
from .views import (
    home,
    BookingListView,
    BookingDetailView,
    BookingCreateView,
    BookingUpdateView,
    BookingDeleteView,
    ReviewListView,
    ReviewCreateView,
    ReviewDeleteView,
    register_user,
)

urlpatterns = [
    path("", home, name="home"),
    # Bookings
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path(
        "bookings/<int:pk>/",
        BookingDetailView.as_view(),
        name="booking_detail",
    ),
    path(
        "bookings/create/", BookingCreateView.as_view(), name="booking_create"
    ),
    path(
        "bookings/update/<int:pk>/",
        BookingUpdateView.as_view(),
        name="booking_update",
    ),
    path(
        "bookings/delete/<int:pk>/",
        BookingDeleteView.as_view(),
        name="booking_delete",
    ),
    # Reviews
    path("reviews/", ReviewListView.as_view(), name="review_list"),
    path("reviews/create/", ReviewCreateView.as_view(), name="review_create"),
    path(
        "reviews/delete/<int:pk>/",
        ReviewDeleteView.as_view(),
        name="review_delete",
    ),
    # User Registration
    path("accounts/register/", register_user, name="register_user"),
]
