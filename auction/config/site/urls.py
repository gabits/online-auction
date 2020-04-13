# Django
from django.contrib import admin
from django.urls import path, include

# Local
from config.api import urls as api_urls

app_name = 'site_config'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls, namespace='api')),
]
