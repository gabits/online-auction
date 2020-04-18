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

    class Meta:
        model = AuctionItem


class AuctionBidFactory(DjangoModelFactory):
    item = AuctionItemFactory()
    price = LazyAttribute(lambda obj: str(fake.pydecimal(right_digits=2)))
    user = SubFactory(UserProfileFactory)

    class Meta:
        model = AuctionBid
