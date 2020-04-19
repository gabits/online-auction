# Third-party
from rest_framework import serializers

# Local
from auction.models import Lot


# Serializers used are all hyperlinked to follow REST API guidelines.
class BaseLotSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name="api:account:v1:user_detail",
        lookup_field="public_id",
        lookup_url_kwarg="public_id"
    )
    username = serializers.SerializerMethodField()
    bids = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="api:auction:v1:lot:bidding_history"
    )

    class Meta:
        model = Lot
        read_only_fields = (
            "public_id",
            "created_at",
            "user",
            "is_active",
            'username',
        )
        fields = (
            "name",
            "base_price",
            "base_price_currency",
            "condition",
        )

    def get_username(self, obj) -> str:
        return obj.user.auth_user.username


class LotListSerializer(BaseLotSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:auction:v1:lots:retrieve_update_destroy",
        lookup_field="public_id"
    )

    class Meta:
        model = BaseLotSerializer.Meta.model
        read_only_fields = BaseLotSerializer.Meta.read_only_fields + (
            'detail_url',
        )
        fields = read_only_fields + BaseLotSerializer.Meta.fields


class LotDetailSerializer(BaseLotSerializer):

    class Meta:
        model = BaseLotSerializer.Meta.model
        read_only_fields = BaseLotSerializer.Meta.read_only_fields + (
            "bids",
            "highest_bid",
            "modified_at",
        )
        fields = read_only_fields + BaseLotSerializer.Meta.fields + (
            "description",
        )
