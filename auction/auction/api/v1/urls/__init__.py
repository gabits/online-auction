# Django
from django.urls import include, path

# Local
import auction.api.v1.urls.lot as lot_urls

app_name = 'v1'

urlpatterns = [
    path('lots/', include(lot_urls, namespace='lots')),
]
