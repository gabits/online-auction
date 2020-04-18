# Django
from django.conf import settings
from django.db.models.signals import post_save

# Local
from django.dispatch import receiver

from common.models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(
        sender, instance=None, created=False, **kwargs
):
    """
    Create a UserProfile for the application to store data on instead of the
    AUTH_USER_MODEL, so we can keep authentication and credentials separate
    from application logic.

    This pattern is put in place to try ensure encapsulation principles and
    separation of concerns.
    """
    if created or (
            not hasattr(instance, "user_profile")
            or instance.user_profile is None
    ):
        UserProfile.objects.create(
            auth_user=instance
        )
