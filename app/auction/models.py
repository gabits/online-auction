# Python standard
import uuid

# Django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Third-party
from djmoney.models.fields import MoneyField
from softdelete.models import SoftDeleteModel

# Local
from account.models import UserProfile


class Lot(SoftDeleteModel):
    """
    Store an individual item placed for auction by a user.
    """
    NEW_UNOPENED = "NEW_UNOPENED"
    NEW_UNUSED = "NEW_UNUSED"
    USED = "USED"
    DEFECTIVE = "DEFECTIVE"
    CONDITION_CHOICES = (
        (NEW_UNOPENED, "New - unopened"),
        (NEW_UNUSED, "New - opened but unused"),
        (USED, "Used"),
        (DEFECTIVE, "Requires service or repair")
    )
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    user = models.ForeignKey(
        UserProfile,
        null=True,
        related_name="lots",
        on_delete=models.SET_NULL,
        help_text="Lot owner.",
        db_index=True
    )
    name = models.CharField(max_length=255)
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255)
    description = models.TextField(
        null=True,
        help_text="Description of the item for auction."
    )
    base_price = MoneyField(
        default="0.00",
        max_digits=19,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        help_text="Starting price for the auction.",
    )
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()

    class Meta:
        # Index the database table first by user, then by
        # latest time of lot creation.
        indexes = [
            models.Index(fields=['user', '-created_at'])
        ]

    @property
    def highest_bid(self):
        return self.bids.order_by("price").last()


class Bid(SoftDeleteModel):
    """
    Record a bid made by a user for a lot.
    """
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    user = models.ForeignKey(
        UserProfile,
        related_name="bids",
        on_delete=models.CASCADE,
        help_text="Bidding user."
    )
    lot = models.ForeignKey(
        Lot,
        related_name="bids",
        on_delete=models.CASCADE
    )
    price = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        help_text=(
            "The bidding price offered, stored in 2 decimal places. "
            "Default currency is in Sterling Pounds."
        )
    )
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        # Index the database table first by user, then by most recent
        # submission time, which means the bid is higher.
        indexes = [
            models.Index(fields=['lot', '-submitted_at'])
        ]


class Sale(models.Model):
    """
    Record a sale once an auction is closed and the respective winning bid.
    """
    lot = models.OneToOneField(
        Lot,
        related_name="sale_record",
        on_delete=models.CASCADE,
    )
    bid = models.OneToOneField(
        Bid,
        null=True,
        related_name="sale_record",
        on_delete=models.CASCADE,
        help_text="The winning bid."
    )
    closed_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time (in UTC) of when the sale was done.",
        # Index the table by time of sale closure.
        db_index=True
    )
