# Django
from django.contrib import admin
from django.urls import path, include, re_path

# Local
from django.views.generic import RedirectView

from config.api import urls as api_urls

app_name = 'site'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls, namespace='api')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # Redirect all URLs to the admin site.
    re_path('^$', RedirectView.as_view(url='admin'), name='home'),
]
