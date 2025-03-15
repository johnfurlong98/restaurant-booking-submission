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
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Review, Table, Reservation
from .forms import BookingForm, ReviewForm, CustomUserCreationForm, ReservationForm
from .mixins import StaffOrOwnerMixin, SuccessMessageMixin, ErrorMessageMixin
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect


def home(request):
    """
    Landing page. Anyone can create a booking from "Make a Booking",
    or they can register/log in if they want advanced features.
    """
    all_reviews = Review.objects.select_related('user').order_by('-created_on')
    return render(request, "reservations/home.html", {'all_reviews': all_reviews})


# ==============
#   BOOKING
# ==============
class BookingListView(StaffOrOwnerMixin, ListView):
    """
    For staff or logged-in users to see all (or filtered) bookings.
    Staff can see all bookings; regular users see only their own.
    """
    model = Booking
    template_name = "reservations/booking_list.html"
    context_object_name = "bookings"
    ordering = ["reservation_date"]


class BookingDetailView(StaffOrOwnerMixin, DetailView):
    """
    Detailed view of one booking.
    Staff can view all; regular users can view only their own.
    """
    model = Booking
    template_name = "reservations/booking_detail.html"
    context_object_name = "booking"


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


class BookingUpdateView(StaffOrOwnerMixin, SuccessMessageMixin, ErrorMessageMixin, UpdateView):
    """
    Only staff or the booking's user can edit.
    """
    model = Booking
    form_class = BookingForm
    template_name = "reservations/booking_update.html"
    success_url = reverse_lazy("booking_list")
    success_message = "Booking updated successfully!"


class BookingDeleteView(StaffOrOwnerMixin, SuccessMessageMixin, DeleteView):
    """
    Only staff or the booking's user can delete.
    """
    model = Booking
    template_name = "reservations/booking_delete.html"
    success_url = reverse_lazy("booking_list")
    success_message = "Booking deleted successfully!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_date'] = self.object.reservation_date.strftime('%B %d, %Y at %I:%M %p')
        return context


# ==============
#   REVIEWS
# ==============
class ReviewListView(StaffOrOwnerMixin, ListView):
    """
    List all reviews. Staff can see all; regular users see their own.
    """
    model = Review
    template_name = "reservations/review_list.html"
    context_object_name = "reviews"
    ordering = ["-created_on"]


class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Only logged-in users can create a review.
    """
    model = Review
    form_class = ReviewForm
    template_name = "reservations/review_create.html"
    success_url = reverse_lazy("review_list")
    success_message = "Review posted successfully!"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReviewDeleteView(StaffOrOwnerMixin, SuccessMessageMixin, DeleteView):
    """
    Only staff or the review's owner can delete a review.
    """
    model = Review
    template_name = "reservations/review_delete.html"
    success_url = reverse_lazy("review_list")
    success_message = "Review deleted successfully!"


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
            login(request, user)
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

    # Get recent bookings
    recent_bookings = Booking.objects.select_related('user').order_by(
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
        'recent_bookings': recent_bookings,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, 'reservations/admin_dashboard.html', context)


# ==============
#   RESERVATIONS
# ==============
class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservations/reservation_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = get_object_or_404(Table, pk=self.kwargs['table_id'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['table'] = get_object_or_404(Table, pk=self.kwargs['table_id'])
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReservationCancelView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reservation
    fields = ['status']
    template_name = 'reservations/reservation_cancel.html'
    success_url = reverse_lazy('reservation_list')
    success_message = "Reservation cancelled successfully!"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = 'cancelled'
        self.object.save()
        messages.success(request, self.success_message)
        return HttpResponseRedirect(self.success_url)
