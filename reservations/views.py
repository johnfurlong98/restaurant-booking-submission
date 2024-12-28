# reservations/views.py

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Booking, Review
from .forms import BookingForm, ReviewForm, CustomUserCreationForm


def home(request):
    """
    Landing page. Anyone can create a booking from "Make a Booking",
    or they can register/log in if they want advanced features.
    """
    return render(request, 'reservations/home.html')


# ==============
#   BOOKING
# ==============
class BookingListView(LoginRequiredMixin, ListView):
    """
    For staff or logged-in users to see all (or filtered) bookings.
    Staff can see all bookings; regular users see only their own.
    """
    model = Booking
    template_name = 'reservations/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all().order_by('reservation_date')
        else:
            return Booking.objects.filter(user=self.request.user).order_by('reservation_date')


class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    Detailed view of one booking.
    Staff can view all; regular users can view only their own.
    """
    model = Booking
    template_name = 'reservations/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=self.request.user)


class BookingCreateView(CreateView):
    """
    Anyone can create a booking (no login required).
    If user is logged in, attach user to the booking automatically.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/booking_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # If user is logged in, link the booking to them
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        messages.success(self.request, "Your booking has been created successfully!")
        return super().form_valid(form)


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Only staff or the booking's user can edit.
    """
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/booking_update.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your booking has been updated successfully!")
        return super().form_valid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Only staff or the booking's user can delete.
    """
    model = Booking
    template_name = 'reservations/booking_delete.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your booking has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ==============
#   REVIEWS
# ==============
class ReviewListView(LoginRequiredMixin, ListView):
    """
    List all reviews. Staff can see all; regular users see their own.
    """
    model = Review
    template_name = 'reservations/review_list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all().order_by('-created_on')
        else:
            return Review.objects.filter(user=self.request.user).order_by('-created_on')


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Only logged-in users can create a review.
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reservations/review_create.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Thank you for your review!")
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """
    Only staff or the review's owner can delete a review.
    """
    model = Review
    template_name = 'reservations/review_delete.html'
    success_url = reverse_lazy('review_list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your review has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ==============
#   USER REGISTRATION
# ==============
def register_user(request):
    """
    A simple registration view that allows any user to sign up without admin approval.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, "Your account has been created and you're now logged in.")
            return redirect('home')
        else:
            messages.error(request, "There was an error with your registration. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'reservations/register.html', {'form': form})
