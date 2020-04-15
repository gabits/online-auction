# Python standard
import uuid

# Django
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


class UserProfile(models.Model):
    """
    Map a Django auth user (used to store credentials and session information)
    to an internal profile used by the application to store business logic.
    """
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    auth_user = models.OneToOneField(
        AUTH_USER_MODEL,
        related_name="user_profile",
        on_delete=models.CASCADE,
    )
