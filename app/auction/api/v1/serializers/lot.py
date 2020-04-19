# Third-party
from typing import Optional

from django.urls import reverse
from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

# Local
from account.api.v1.serializers import BaseRelatedUserSerializer
from auction.models import Bid, Lot


class BaseLotSerializer(BaseRelatedUserSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Lot
        read_only_fields = BaseRelatedUserSerializer.Meta.read_only_fields + (
            "public_id",
            "created_at",
            "user",
            "is_active",
        )
        fields = (
            "name",
            "base_price",
            "base_price_currency",
            "condition",
            "expires_at"
        )

    def get_is_active(self, object) -> bool:
        return object.is_active


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
    highest_bid = serializers.SerializerMethodField()
    highest_bid_price = MoneyField(
        source="highest_bid.price",
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        model = BaseLotSerializer.Meta.model
        read_only_fields = BaseLotSerializer.Meta.read_only_fields + (
            "bids",
            "highest_bid",
            "highest_bid_price",
            "modified_at",
        )
        fields = read_only_fields + BaseLotSerializer.Meta.fields + (
            "description",
        )

    def _get_highest_bid(self, object) -> Optional[Bid]:
        return object.highest_bid

    def get_highest_bid(self, object) -> str:
        highest_bid = self._get_highest_bid(object)
        view_name = "api:auction:v1:bids:retrieve"
        path = reverse(
            view_name, kwargs={"bid_public_id": highest_bid.public_id}
        )
        url = self.context["request"].build_absolute_uri(path)
        return url

    def get_bids(self, object) -> str:
        view_name = "api:auction:v1:lot:bid_history"
        path = reverse(view_name, kwargs={"lot_public_id": object.public_id})
        url = self.context["request"].build_absolute_uri(path)
        return url
