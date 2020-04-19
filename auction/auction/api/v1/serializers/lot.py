# Third-party
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
        read_only_fields = (
            "public_id",
            "created_at",
            "user",
            "highest_bid",
            "bids",
            "sale_record",
            "modified_at",
        )
        fields = read_only_fields + (
            "base_price",
            "base_price_currency",
            "is_active",
            "name",
            "description",
        )
