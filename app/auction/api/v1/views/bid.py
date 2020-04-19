# Django
from django.shortcuts import get_object_or_404

# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_condition import C, ConditionalPermission
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

# Local
from auction.api.v1.serializers import (
    BidDetailSerializer,
    BidListCreateSerializer
)
from auction.models import Bid, Lot
from auction.permissions import IsLotObjectOwner, IsReadyOnlyRequest


class BidListAPIView(ListCreateAPIView):
    """
    GET requests to this endpoint will return a list of all existing bids
    for a lot. Results can be ordered and queried by relevant fields, such as
    price offered, time submitted or user.

    POST requests to this endpoint will submit a bid for this lot, which must
    provide a higher price than the current highest bid.
    """
    permission_classes = [ConditionalPermission, ]
    permission_condition = (
        (C(IsAuthenticated)) & (
            (C(IsReadyOnlyRequest)) | (~C(IsLotObjectOwner))
        )
    )
    serializer_class = BidListCreateSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []

    def perform_create(self, serializer):
        """
        Save a new instance created, linking to it the requesting user.
        """
        serializer.save(user=self.request.user.user_profile)

    def get_queryset(self):
        """
        Extend Django's default method so we can also check for lot
        permissions against the user and filter the `Bid`s list by a
        specific lot.
        """
        lot_public_id = self.kwargs["lot_public_id"]
        lot = get_object_or_404(Lot, public_id=lot_public_id)
        self.check_object_permissions(self.request, lot)
        return Bid.objects.filter(lot=lot)

    def get_serializer(self, *args, **kwargs):
        """
        Provide an identifier the respective bid lot to the serializer
        instance by extending Django's default method.
        """
        data = kwargs.get("data", {})
        # Mutate the data dictionary so we can provide the lot `public_id`
        data.update({"lot": self.kwargs["lot_public_id"]})
        return super().get_serializer(*args, **kwargs)


class BidRetrieveAPIView(RetrieveAPIView):
    serializer_class = BidDetailSerializer
    queryset = Bid.objects.all()
    lookup_field = "public_id"
    lookup_url_kwarg = "bid_public_id"
