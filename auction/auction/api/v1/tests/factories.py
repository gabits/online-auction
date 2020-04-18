# Third-party
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

# Local
from auction.models import AuctionBid, AuctionItem
from common.tests.factories import UserProfileFactory

fake = Faker()


# Factories to facilitate testing logic.
class AuctionItemFactory(DjangoModelFactory):
    user = SubFactory(UserProfileFactory)
    name = LazyAttribute(lambda obj: fake.sentence())
    description = LazyAttribute(lambda obj: fake.text())
    is_active = LazyAttribute(lambda obj: fake.pybool())
    base_price = LazyAttribute(
        lambda obj: str(
            fake.pydecimal(right_digits=2, min_value=0.00, max_value=1000.00)
        )
    )

    class Meta:
        model = AuctionItem


class AuctionBidFactory(DjangoModelFactory):
    item = AuctionItemFactory()
    price = LazyAttribute(
        lambda obj: str(
            fake.pydecimal(right_digits=2, min_value=0.00, max_value=1000.00)
        )
    )
    user = SubFactory(UserProfileFactory)

    class Meta:
        model = AuctionBid
