# reservations/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Booking, Review, Table
from .forms import BookingForm, ReviewForm, CustomUserCreationForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta


def home(request):
    """
    Landing page. Anyone can create a booking from "Make a Booking",
    or they can register/log in if they want advanced features.
    """
    return render(request, "reservations/home.html")


# ==============
#   BOOKING
# ==============
class BookingListView(LoginRequiredMixin, ListView):
    """
    For staff or logged-in users to see all (or filtered) bookings.
    Staff can see all bookings; regular users see only their own.
    """

    model = Booking
    template_name = "reservations/booking_list.html"
    context_object_name = "bookings"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all().order_by("reservation_date")
        else:
            return Booking.objects.filter(user=self.request.user).order_by(
                "reservation_date"
            )


class BookingDetailView(LoginRequiredMixin, DetailView):
    """
    Detailed view of one booking.
    Staff can view all; regular users can view only their own.
    """

    model = Booking
    template_name = "reservations/booking_detail.html"
    context_object_name = "booking"

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
    template_name = "reservations/booking_create.html"
    success_url = reverse_lazy("booking_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Check for existing non-expired bookings
            existing_booking = Booking.objects.filter(
                user=self.request.user,
                reservation_date__gte=timezone.now()
            ).order_by('reservation_date').first()
            
            if existing_booking:
                context['existing_booking'] = existing_booking
                context['has_existing_booking'] = True
            else:
                context['has_existing_booking'] = False
        return context

    def form_valid(self, form):
        try:
            if self.request.user.is_authenticated:
                form.instance.user = self.request.user
            response = super().form_valid(form)
            messages.success(
                self.request,
                f"Booking created successfully for {form.instance.reservation_date.strftime('%B %d, %Y at %I:%M %p')}!"
            )
            return response
        except Exception as e:
            messages.error(
                self.request,
                f"Error creating booking: {str(e)}"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"Error in {field}: {error}"
                )
        return super().form_invalid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse_lazy("booking_list")
        return reverse_lazy("home")


class BookingUpdateView(LoginRequiredMixin, UpdateView):
    """
    Only staff or the booking's user can edit.
    """

    model = Booking
    form_class = BookingForm
    template_name = "reservations/booking_update.html"
    success_url = reverse_lazy("booking_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(
                self.request,
                f"Booking updated successfully for {form.instance.reservation_date.strftime('%B %d, %Y at %I:%M %p')}!"
            )
            return response
        except Exception as e:
            messages.error(
                self.request,
                f"Error updating booking: {str(e)}"
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"Error in {field}: {error}"
                )
        return super().form_invalid(form)


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Only staff or the booking's user can delete.
    """

    model = Booking
    template_name = "reservations/booking_delete.html"
    success_url = reverse_lazy("booking_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        try:
            booking = self.get_object()
            booking_date = booking.reservation_date.strftime('%B %d, %Y at %I:%M %p')
            response = super().delete(request, *args, **kwargs)
            messages.success(
                self.request,
                f"Booking for {booking_date} has been deleted successfully!"
            )
            return response
        except Exception as e:
            messages.error(
                self.request,
                f"Error deleting booking: {str(e)}"
            )
            return redirect('booking_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_date'] = self.object.reservation_date.strftime('%B %d, %Y at %I:%M %p')
        return context


# ==============
#   REVIEWS
# ==============
class ReviewListView(LoginRequiredMixin, ListView):
    """
    List all reviews. Staff can see all; regular users see their own.
    """

    model = Review
    template_name = "reservations/review_list.html"
    context_object_name = "reviews"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all().order_by("-created_on")
        else:
            return Review.objects.filter(user=self.request.user).order_by(
                "-created_on"
            )


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Only logged-in users can create a review.
    """

    model = Review
    form_class = ReviewForm
    template_name = "reservations/review_create.html"
    success_url = reverse_lazy("review_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Review posted successfully!")
        return response


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """
    Only staff or the review's owner can delete a review.
    """

    model = Review
    template_name = "reservations/review_delete.html"
    success_url = reverse_lazy("review_list")

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, "Your review has been deleted successfully!"
        )
        return super().delete(request, *args, **kwargs)


# ==============
#   USER REGISTRATION
# ==============
@ensure_csrf_cookie
def register_user(request):
    """
    A simple registration view that allows any user to sign up without admin approval.
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(
                request, user
            )  # Automatically log in the user after registration
            messages.success(
                request,
                "Your account has been created and you're now logged in.",
            )
            return redirect("home")
        else:
            messages.error(
                request,
                "There was an error with your registration. Please correct the errors below.",
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "reservations/register.html", {"form": form})


@staff_member_required
def admin_dashboard(request):
    """
    Admin dashboard showing key statistics and recent activity
    """
    # Calculate statistics
    total_bookings = Booking.objects.count()
    todays_bookings = Booking.objects.filter(
        reservation_date__date=timezone.now().date()
    ).count()
    total_users = User.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0

    # Get bookings for the next 7 days
    next_week = timezone.now() + timedelta(days=7)
    upcoming_bookings = Booking.objects.filter(
        reservation_date__range=(timezone.now(), next_week)
    ).count()

    # Get table utilization
    table_stats = Table.objects.annotate(
        booking_count=Count('bookings')
    ).order_by('-booking_count')[:5]

    # Get recent bookings with more details
    recent_bookings = Booking.objects.select_related('table', 'user').order_by(
        '-created_on'
    )[:10]

    # Get recent reviews
    recent_reviews = Review.objects.select_related('user').order_by(
        '-created_on'
    )[:5]

    context = {
        'total_bookings': total_bookings,
        'todays_bookings': todays_bookings,
        'total_users': total_users,
        'avg_rating': avg_rating,
        'upcoming_bookings': upcoming_bookings,
        'table_stats': table_stats,
        'recent_bookings': recent_bookings,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'reservations/admin_dashboard.html', context)
