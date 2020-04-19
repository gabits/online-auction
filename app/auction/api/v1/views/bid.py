# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

# Local
from auction.api.v1.serializers import BidListSerializer
from auction.models import Bid


class BidListAPIView(ListCreateAPIView):
    """
    GET requests to this endpoint will return a list of all existing bids
    for a lot. Results can be ordered and queried by relevant fields, such as
    price offered, time submitted or user.

    POST requests to this endpoint will submit a bid for this lot, which must
    provide a higher price than the current highest bid.
    """
    queryset = Bid.objects.all()
    lookup_field = "lot"
    permission_classes = (IsAuthenticated, )
    serializer_class = BidListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = []
    search_fields = []
    ordering_fields = []

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user_profile)
