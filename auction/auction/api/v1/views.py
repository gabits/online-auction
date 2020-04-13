# Third-party
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView


class TestAPIView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "Not implemented."},
            status=status.HTTP_200_OK
        )
