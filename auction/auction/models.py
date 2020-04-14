import uuid

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField


class AuctionItem(models.Model):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)


class AuctionBid(models.Model):
    public_id = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        help_text="Public identifier to be exposed in the API."
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="bids",
        on_delete=models.SET_NULL,
        null=True
    )
    submitted_at = models.DateTimeField(default=timezone.now)
    price = MoneyField(
        max_digits=19,
        decimal_places=2,
        default_currency="GBP"
    )
