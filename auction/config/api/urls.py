# Django
from django.urls import path, include

# Local
from auction import urls as auction_urls

urlpatterns = [
    path('auction/', include(auction_urls, namespace='auction'))
]
