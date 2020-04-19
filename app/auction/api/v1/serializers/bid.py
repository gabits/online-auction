# Third-party
from rest_framework import serializers

# Local
from account.api.v1.serializers import BaseRelatedUserSerializer
from auction.models import Bid, Lot


class BaseBidSerializer(BaseRelatedUserSerializer):
    lot = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=Lot.objects.all(),
        write_only=True,
    )

    class Meta:
        model = Bid
        read_only_fields = BaseRelatedUserSerializer.Meta.read_only_fields
        fields = read_only_fields + (
            "price",
            "lot",
        )


class BidListCreateSerializer(BaseBidSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:auction:v1:bids:retrieve",
        lookup_field="public_id",
        lookup_url_kwarg="bid_public_id"
    )

    class Meta:
        model = BaseBidSerializer.Meta.model
        read_only_fields = BaseBidSerializer.Meta.read_only_fields + (
            "detail_url",
        )
        fields = read_only_fields + BaseBidSerializer.Meta.fields


class BidDetailSerializer(BaseBidSerializer):

    class Meta:
        model = BaseBidSerializer.Meta.model
        read_only_fields = BaseBidSerializer.Meta.read_only_fields + (
            "public_id",
            "created_at",
        )
        fields = read_only_fields + BaseBidSerializer.Meta.fields
