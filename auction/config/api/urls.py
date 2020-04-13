# Django
from django.urls import path, include

# Local
from auction.api import urls as auction_api_urls

app_name = 'api_config'

urlpatterns = [
    path('auction/', include(auction_api_urls, namespace='auction'))
]
