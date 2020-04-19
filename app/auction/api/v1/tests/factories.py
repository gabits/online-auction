# Third-party
from datetime import timedelta

from django.utils import timezone
from factory import LazyAttribute, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Faker

# Local
from auction.models import Bid, Lot
from account.tests.factories import UserProfileFactory

fake = Faker()


# Factories to facilitate testing logic.
class LotFactory(DjangoModelFactory):
    user = SubFactory(UserProfileFactory)
    name = LazyAttribute(lambda obj: fake.sentence())
    description = LazyAttribute(lambda obj: fake.text())
    base_price = LazyAttribute(
        lambda obj: str(
            fake.pydecimal(right_digits=2, min_value=0.00, max_value=1000.00)
        )
    )
    condition = fuzzy.FuzzyChoice(Lot.CONDITION_CHOICES)
    expires_at = LazyAttribute(
        lambda obj: timezone.now() + timedelta(seconds=300)
    )

    class Meta:
        model = Lot


class BidFactory(DjangoModelFactory):
    lot = LotFactory()
    price = LazyAttribute(
        lambda obj: str(
            fake.pydecimal(right_digits=2, min_value=0.00, max_value=1000.00)
        )
    )
    user = SubFactory(UserProfileFactory)

    class Meta:
        model = Bid
