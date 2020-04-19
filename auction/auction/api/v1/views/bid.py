# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

# Local
from auction.api.v1.serializers.bid import AuctionBidListSerializer
from auction.models import AuctionBid


class LotBidListAPIView(ListCreateAPIView):
    """
    GET requests to this endpoint will return a list of all existing bids
    for a lot. Its results can be queried by fields such as active or
    inactive items, which can also be ordered.

    POST requests to this endpoint will submit a bid for this auction item,
    which must provide a higher price than the current highest bid.
    """
    queryset = AuctionBid.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AuctionBidListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user_profile)
