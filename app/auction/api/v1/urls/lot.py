# Django
from django.conf import settings
from django.urls import re_path

# Local
from auction.api.v1 import views

app_name = 'v1'

urlpatterns = [
    re_path(
        '^$', views.LotListAPIView.as_view(),
        name='list_create'
    ),
    re_path(
        f'^(?P<public_id>{settings.UUID_REGEX_FORMAT})$',
        views.LotRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_update_destroy'
    ),
    # Collection endpoint for lot bids
    re_path(
        f'^(?P<public_id>{settings.UUID_REGEX_FORMAT})/bids$',
        views.BidListAPIView.as_view(),
        name='bid'
    ),
]
