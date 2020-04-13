# Django
from django.conf.urls import url

# Local
from auction.api.v1 import views

app_name = 'v1'

urlpatterns = [
    url(r'test', views.MockAPIView.as_view(), name='mock_view'),
]
