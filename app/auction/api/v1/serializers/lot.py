# Third-party
from rest_framework import serializers

# Local
from auction.models import Lot


# Serializers used are all hyperlinked to follow REST API guidelines.
#
# TODO: Change this ModelSerializer to a HyperlinkedModelSerializer after
#  /bids/ and /user/ endpoints are implemented so we can hyperlink them
class LotListSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name="account"
    )

    class Meta:
        model = Lot
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
            "is_active",
            "condition",
            "expiration_time"
        )


class LotDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lot
        read_only_fields = (
            "public_id",
            "created_at",
            "user",
            "highest_bid",
            # TODO: remove this
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
            "condition"
        )
