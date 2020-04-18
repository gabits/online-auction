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
from common.models import UserProfile


class AuctionItem(SoftDeleteModel):
    """
    Store an individual item placed for auction by a user.
    """
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    user = models.ForeignKey(
        UserProfile,
        null=True,
        related_name="auction_items",
        on_delete=models.SET_NULL,
        help_text="Item owner.",
        db_index=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, help_text="Item description.")
    base_price = MoneyField(
        default="0.00",
        max_digits=19,
        decimal_places=2,
        default_currency=settings.DEFAULT_CURRENCY,
        help_text="Starting price for the auction.",
    )
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    class Meta:
        # Index the database table first by user, then by
        # latest time of items creation.
        indexes = [
            models.Index(fields=['user', '-created_at'])
        ]


class AuctionBid(SoftDeleteModel):
    """
    Record a bid made by a user on an auction item.
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
    item = models.ForeignKey(
        AuctionItem,
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
    # Store if this is the highest bid for the item.
    # Defined here to prevent circular dependencies and keep consistency
    # with the other foreign keys defined.
    winning_item = models.OneToOneField(
        AuctionItem,
        null=True,
        related_name="highest_bid",
        on_delete=models.PROTECT
    )

    class Meta:
        # Index the database table first by user, then by most recent
        # submission time, which means the bid is higher.
        indexes = [
            models.Index(fields=['item', '-submitted_at'])
        ]


class Sale(models.Model):
    """
    Record a sale once an auction is closed and the respective winning bid.
    """
    item = models.OneToOneField(
        AuctionItem,
        related_name="sale_record",
        on_delete=models.CASCADE,
    )
    bid = models.OneToOneField(
        AuctionBid,
        null=True,
        related_name="sale_record",
        on_delete=models.CASCADE,
        help_text="The winning bid."
    )
    closed_at = models.DateTimeField(
        default=timezone.now,
        help_text="Date and time (aware) of when the sale was done.",
        # Index the table by time of sale closure.
        db_index=True
    )
