# Django
from django.utils import timezone

# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Local
from auction.api.v1.serializers import (
    AuctionItemDetailSerializer,
    AuctionItemListSerializer,
)
from auction.models import AuctionItem


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


class AuctionItemRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
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

    def perform_update(self, serializer):
        serializer.save(modified_at=timezone.now())

    def perform_destroy(self, instance):
        if not instance.is_active:
            super().perform_destroy(instance)
        else:
            raise ValidationError(
                detail={
                    "detail": (
                        "Cannot delete a lot which is currently active. "
                        "Please set it inactive first."
                    )
                }
            )
