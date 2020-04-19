# Django
from django.utils import timezone

# Third-party
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

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
    # TODO: permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = LotListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = (
        'user__public_id',
        'name',
        'expires_at',
        'base_price_currency'
    )
    search_fields = ('name', 'description', 'base_price')
    ordering_fields = (
        'name',
        'created_at',
        'modified_at',
        'base_price',
        'expires_at'
    )

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
    lookup_field = "public_id"
    lookup_url_kwarg = "lot_public_id"
    serializer_class = LotDetailSerializer

    def perform_update(self, serializer):
        """
        If the instance has valid modifications to be performed, save them and
        record that it has been modified.
        """
        if serializer.validated_data:
            serializer.save(modified_at=timezone.now())

    def get_object(self):
        object = super().get_object()
        self._validate_inactive_instance(object)
        return object

    def _validate_inactive_instance(self, instance):
        if not instance.is_active:
            raise ValidationError(
                detail={
                    "detail": (
                        "Cannot update neither delete a lot which is no "
                        "longer active."
                    )
                }
            )
