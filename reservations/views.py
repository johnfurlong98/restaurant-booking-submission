from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm

def home(request):
    return render(request, 'reservations/home.html')  # or any template name

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'reservations/booking_list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('reservation_date')

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'reservations/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/booking_create.html'
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Booking created successfully!")
        return super().form_valid(form)

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'reservations/booking_update.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Booking updated successfully!")
        return super().form_valid(form)

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'reservations/booking_delete.html'
    success_url = reverse_lazy('booking_list')

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Booking deleted successfully!")
        return super().delete(request, *args, **kwargs)
