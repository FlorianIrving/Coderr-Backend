from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended user profile model linked to Django's built-in User.
    Stores additional personal and business-related information.
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    # First name of the user (optional)
    first_name = models.CharField(max_length=100, blank=True, default="")
    # Last name of the user (optional)
    last_name = models.CharField(max_length=100, blank=True, default="")
    # Optional profile picture uploaded to 'profile_pics/' directory
    file = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    # Location or address information (optional)
    location = models.CharField(max_length=100, blank=True, default="")
    # Telephone number (optional)
    tel = models.CharField(max_length=30, blank=True, default="")
    # Short description or bio of the user (optional)
    description = models.TextField(blank=True, default="")
    # Working hours or availability description (optional)
    working_hours = models.CharField(max_length=100, blank=True, default="")
    # User type or role, e.g., 'freelancer', 'client' (optional)
    type = models.CharField(max_length=50, blank=True, default="")

    # Timestamp of profile creation
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Returns a readable representation of the profile instance
        return f"Profile of {self.user.username}"
