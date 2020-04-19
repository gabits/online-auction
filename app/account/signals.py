# Django
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Local
from account.models import UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(
        sender, instance=None, **kwargs
):
    """
    Create a UserProfile for the application to store data on instead of the
    AUTH_USER_MODEL, so we can keep authentication and credentials separate
    from application logic.

    This pattern is put in place to try ensure encapsulation principles and
    separation of concerns.
    """
    if (
        not hasattr(instance, "user_profile")
        or instance.user_profile is None
    ):
        UserProfile.objects.create(
            auth_user=instance
        )
