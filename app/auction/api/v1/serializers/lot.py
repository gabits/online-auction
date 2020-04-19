# Third-party
from django.urls import reverse
from rest_framework import serializers

# Local
from account.api.v1.serializers import BaseRelatedUserSerializer
from auction.models import Lot


class BaseLotSerializer(BaseRelatedUserSerializer):

    class Meta:
        model = Lot
        read_only_fields = BaseRelatedUserSerializer.Meta.read_only_fields + (
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


class LotListSerializer(BaseLotSerializer):
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="api:auction:v1:lots:retrieve_update_destroy",
        lookup_field="public_id",
        lookup_url_kwarg="lot_public_id"
    )

    class Meta:
        model = BaseLotSerializer.Meta.model
        read_only_fields = BaseLotSerializer.Meta.read_only_fields + (
            'detail_url',
        )
        fields = read_only_fields + BaseLotSerializer.Meta.fields


class LotDetailSerializer(BaseLotSerializer):
    bids = serializers.SerializerMethodField()

    def get_bids(self, object) -> str:
        view_name = "api:auction:v1:lot:bidding_history"
        path = reverse(view_name, kwargs={"lot_public_id": object.public_id})
        url = self.context["request"].build_absolute_uri(path)
        return url

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
