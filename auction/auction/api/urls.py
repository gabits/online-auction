# Django
from django.urls import path, include

# Local
from auction.api.v1 import urls as v1_urls

app_name = 'auction'

# Route to different versions of the API, following REST principles.
urlpatterns = [
    path('v1/', include(v1_urls, namespace='v1'))
]
