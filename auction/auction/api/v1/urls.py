# Django
from django.conf import settings
from django.conf.urls import url

# Local
from auction.api.v1 import views

app_name = 'v1'

urlpatterns = [
    url(
        f'lot/(?P<public_id>{settings.UUID_REGEX_FORMAT})$',
        views.AuctionItemRetrieveUpdateDestroyAPIView.as_view(),
        name='lot_retrieve_update_destroy'
    ),
    url(
        r'lot$',
        views.AuctionItemListAPIView.as_view(),
        name='lot_list_create'
    ),
]
