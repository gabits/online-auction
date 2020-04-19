# Django
from django.conf import settings
from django.urls import re_path

# Local
from auction.api.v1 import views

app_name = 'lot'

urlpatterns = [
    re_path(
        '^$', views.LotListAPIView.as_view(),
        name='list_create'
    ),
    re_path(
        f'^(?P<lot_public_id>{settings.UUID_REGEX_FORMAT})$',
        views.LotRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_update_destroy'
    ),
    # Collection endpoint for lot bids
    re_path(
        f'^(?P<lot_public_id>{settings.UUID_REGEX_FORMAT})/history$',
        views.BidListAPIView.as_view(),
        name='bid_history'
    ),
    re_path(
        f'^(?P<lot_public_id>{settings.UUID_REGEX_FORMAT})/bid$',
        views.BidCreateAPIView.as_view(),
        name='bid_create'
    )
]
