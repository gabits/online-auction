# Django
from django.conf import settings
from django.urls import re_path

# Local
from auction.api.v1 import views

app_name = 'v1'

urlpatterns = [
    re_path(
        '$', views.AuctionItemListAPIView.as_view(),
        name='list_create'
    ),
    re_path(
        f'(?P<public_id>{settings.UUID_REGEX_FORMAT})$',
        views.AuctionItemRetrieveUpdateDestroyAPIView.as_view(),
        name='retrieve_update_destroy'
    ),
    re_path(
        f'(?P<public_id>{settings.UUID_REGEX_FORMAT})/bids$',
        views.AuctionItemListAPIView.as_view(),
        name='bid_collection'
    ),
]
