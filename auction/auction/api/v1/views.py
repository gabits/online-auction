# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Local
from auction.api.v1.serializers import (
    AuctionItemListSerializer,
    AuctionItemDetailSerializer,
)
from auction.models import AuctionItem


class MockAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    allowed_methods = ["get", "head", "options"]

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Not implemented."},
            status=status.HTTP_200_OK
        )


class AuctionItemListAPIView(ListCreateAPIView):
    """
    GET requests to this endpoint will return a list of all existing auction
    items. Its results can be queried by fields such as active or
    inactive items, which can also be ordered.

    POST requests to this endpoint will create a single lot (auction item) in
    the system, which are by default inactive - not for auction - unless
    explicitly requested otherwise.
    """
    queryset = AuctionItem.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AuctionItemListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'user', 'created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user_profile)


class AuctionItemRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    """
    GET requests to this endpoint will retrieve an auction item, if the URL
    matches the public_id of an existing one in the system.

    DELETE requests to this endpoint will attempt to delete the auction item
    from the system.
    """
    queryset = AuctionItem.objects.all()
    lookup_field = 'public_id'
    permission_classes = (IsAuthenticated, )
    serializer_class = AuctionItemDetailSerializer
    # TODO: users should only be able to delete an item that is inactive.
