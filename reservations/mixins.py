from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy


class StaffOrOwnerMixin(LoginRequiredMixin):
    """
    Mixin to handle staff or owner access to views
    """
    def get_queryset(self):
        if self.request.user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)


class SuccessMessageMixin:
    """
    Mixin to handle success messages in views
    """
    success_message = None

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response


class ErrorMessageMixin:
    """
    Mixin to handle error messages in views
    """
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request,
                    f"Error in {field}: {error}"
                )
        return super().form_invalid(form) 