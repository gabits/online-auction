from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

from account.api.v1.serializers import (
    UserProfileListSerializer,
    UserProfileDetailSerializer,
)
from account.models import UserProfile


class UserProfileListAPIView(ListAPIView):
    serializer_class = UserProfileListSerializer
    queryset = UserProfile.objects.all()


class MyUserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer

    def get_object(self):
        return self.request.user.user_profile


class UserProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileDetailSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'public_id'
