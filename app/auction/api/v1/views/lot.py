# Django
from django.utils import timezone

# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

# Local
from auction.api.v1.serializers import (
    LotDetailSerializer,
    LotListSerializer,
)
from auction.models import Lot


class LotListAPIView(ListCreateAPIView):
    """
    GET requests to this endpoint will return a list of all existing lots.
    Results can be queried by fields such as active or inactive lots,
    which can also be ordered.

    POST requests to this endpoint will create a single lot (auction item) in
    the system, which are by default inactive - not for auction - unless
    explicitly requested otherwise.
    """
    queryset = Lot.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = LotListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('is_active', 'user__public_id', 'name')
    search_fields = ('name', 'description', 'base_price')
    ordering_fields = ('name', 'created_at', 'modified_at', 'base_price')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user_profile)


class LotRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET requests to this endpoint will retrieve a lot, if the URL matches the
    public_id of an existing one in the system.

    DELETE requests to this endpoint will attempt to delete the lot from the
    system.
    """
    queryset = Lot.objects.all()
    lookup_field = 'public_id'
    permission_classes = (IsAuthenticated, )
    serializer_class = LotDetailSerializer

    def perform_update(self, serializer):
        if serializer.validated_data:
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