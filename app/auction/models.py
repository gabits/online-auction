# Django
from django.conf import settings
from django.db import models
from django.utils import timezone

# Third-party
from djmoney.models.fields import MoneyField

# Local
from account.models import UserProfile
from common.models import GenericApplicationModel


class Auction(GenericApplicationModel):
    """
    Store an auction started by an user.
    """
    user = models.ForeignKey(
        UserProfile,
        null=True,
        related_name="auctions",
        on_delete=models.SET_NULL,
        help_text="Auction owner.",
    )
    base_price = MoneyField(
        default="0.00",
        max_digits=19,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        help_text="Starting price for the auction.",
    )
    expires_at = models.DateTimeField()

    class Meta:
        # Index the database table first by user, then by
        # latest time of auction creation.
        indexes = [
            models.Index(fields=['user', 'created_at'])
        ]

    @property
    def is_active(self):
        return timezone.now() < self.expires_at

    @property
    def highest_bid(self):
        return self.bids.order_by("price").last()


class Lot(GenericApplicationModel):
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
    name = models.CharField(max_length=255)
    condition = models.CharField(choices=CONDITION_CHOICES, max_length=255)
    description = models.TextField(
        null=True,
        help_text="Description of the item for auction."
    )
    # In the future, this can be expanded to a Foreign Key.
    auction = models.OneToOneField(
        Auction,
        related_name="lot",
        db_index=True, on_delete=models.CASCADE
    )


class Bid(GenericApplicationModel):
    """
    Record a bid made by a user for a lot.
    """
    user = models.ForeignKey(
        UserProfile,
        related_name="user",
        on_delete=models.CASCADE,
        help_text="Bidding user."
    )
    auction = models.ForeignKey(
        Auction,
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

    class Meta:
        # Index the database table first by user, then by most recent
        # submission time, which means the bid is higher.
        indexes = [
            models.Index(fields=['auction', 'created_at'])
        ]
