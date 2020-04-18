# Django
from django.conf.urls import url

# Local
from auction.api.v1 import views

app_name = 'v1'

urlpatterns = [
    url(r'test/$', views.MockAPIView.as_view(), name='mock_view'),
    url(
        r'lot/(?P<public_id>[0-9a-z\-]+)$',
        views.AuctionItemRetrieveDestroyAPIView.as_view(),
        name='lot_retrieve_destroy'
    ),
    url(
        r'lot$',
        views.AuctionItemListAPIView.as_view(),
        name='lot_list_create'
    ),
]
