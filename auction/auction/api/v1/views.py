# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auction.api.v1.serializers import AuctionItemListSerializer
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
    List all existing auction items. Results can be queried by some fields -
    such as active or inactive items - and can also be ordered.
    """
    queryset = AuctionItem.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = AuctionItemListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'user', 'created_at']
