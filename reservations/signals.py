from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib import messages

@receiver(user_logged_in)
def notify_user_logged_in(sender, request, user, **kwargs):
    messages.success(request, f"Welcome back, {user.username}!")

@receiver(user_logged_out)
def notify_user_logged_out(sender, request, user, **kwargs):
    # Note: user can be None if the session is timed out. Handle that gracefully:
    username = user.username if user else "User"
    messages.info(request, f"{username}, you have been logged out successfully!")
