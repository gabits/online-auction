# Third-party
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class MockAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    allowed_methods = ["get", "head", "options"]

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {"detail": "Not implemented."},
            status=status.HTTP_200_OK
        )
