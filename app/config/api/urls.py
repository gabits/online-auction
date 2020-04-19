# Django
from django.urls import path, include

# Local
from auction.api import urls as auction_api_urls
from account.api import urls as account_api_urls

app_name = 'api'

urlpatterns = [
    path('auction/', include(auction_api_urls, namespace='auction')),
    path('account/', include(account_api_urls, namespace='account')),
]
