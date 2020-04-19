# Django
from django.conf import settings
from django.urls import re_path

# Local
from auction.api.v1 import views

app_name = 'bid'

urlpatterns = [
    re_path(
        f'^(?P<bid_public_id>{settings.UUID_REGEX_FORMAT})$',
        views.BidRetrieveAPIView.as_view(),
        name='retrieve'
    ),
]
