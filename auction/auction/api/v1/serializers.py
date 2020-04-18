# Third-party
from rest_framework import serializers

from auction.models import AuctionItem


# Serializers used are all hyperlinked to follow REST API guidelines.
class AuctionItemListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AuctionItem
        fields = read_only_fields = (
            "public_id",
            "user",
            "name",
            "highest_bid",
            "created_at"
        )


class AuctionItemDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        many=True,
        read_only=True
    )

    class Meta:
        model = AuctionItem
        read_only_fields = (
            "public_id",
            "highest_bid",
            "created_at"
        )
        fields = read_only_fields + (
            "user",
            "name",
            "description",
            "base_price"
        )
