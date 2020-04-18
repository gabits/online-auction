# Third-party
from django.conf import settings
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

# Local
from auction.models import AuctionItem


# Serializers used are all hyperlinked to follow REST API guidelines.
#
# TODO: Change this ModelSerializer to a HyperlinkedModelSerializer after
#  /bids/ and /user/ endpoints are implemented so we can hyperlink them
class AuctionItemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionItem
        read_only_fields = (
            "public_id",
            "created_at",
            "user",
        )
        fields = read_only_fields + (
            "name",
            "description",
            "base_price",
            "base_price_currency",
            "is_active"
        )


class AuctionItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuctionItem
        fields = read_only_fields = (
            "public_id",
            "created_at",
            "user",
            "name",
            "description",
            "base_price",
            "base_price_currency",
            "is_active",
            "highest_bid",
            "bids",
            "sale_record",
        )
