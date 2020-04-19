# Third-party
from rest_framework import serializers

# Local
from auction.models import Bid, Lot


# Serializers used are all hyperlinked to follow REST API guidelines.
#
# TODO: Change this ModelSerializer to a HyperlinkedModelSerializer after
#  /bids/ and /user/ endpoints are implemented so we can hyperlink them
class BidListSerializer(serializers.ModelSerializer):
    is_highest = serializers.SerializerMethodField(
        help_text="Whether or not this bid is currently the lot's highest."
    )
    lot = serializers.SlugRelatedField(
        slug_field="public_id",
        queryset=Lot.objects.all(),
        write_only=True
    )

    class Meta:
        model = Bid
        read_only_fields = (
            "public_id",
            "user",
            "submitted_at",
            "is_highest",
        )
        fields = read_only_fields + (
            "price",
            "lot",
        )

    def get_is_highest(self, obj) -> bool:
        return bool(obj.highest_for_lot)
