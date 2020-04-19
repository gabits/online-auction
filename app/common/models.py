# Python standard
import uuid
from django.utils import timezone

# Django
from django.db import models

# Third-party
from softdelete.models import SoftDeleteModel


class GenericApplicationModel(SoftDeleteModel):
    """
    Abstract model to implement common elements for all models, such as a
    public UUID to expose in the API and soft deletion for audit log and
    troubleshooting purposes.
    """
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save()
