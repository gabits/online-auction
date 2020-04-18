# Django
from django.contrib import admin
from django.urls import path, include

# Local
from config.api import urls as api_urls

app_name = 'site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls, namespace='api')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
