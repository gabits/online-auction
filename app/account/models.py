# Django
from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models

# Third-party
from softdelete.models import SoftDeleteModel

from common.models import GenericApplicationModel


class UserProfile(GenericApplicationModel):
    """
    Map a Django auth user (used to store credentials and session information)
    to an internal profile used by the application to store business logic.
    """
    auth_user = models.OneToOneField(
        AUTH_USER_MODEL,
        related_name="user_profile",
        on_delete=models.CASCADE,
    )
