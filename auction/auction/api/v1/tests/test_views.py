# Django
from django.test import TestCase

# Local
from common.tests.mixins import APIEndpointTestMixin


class TestMockView(APIEndpointTestMixin):
    url = "api:auction:v1:mock_view"
    supported_http_methods = {"get"}
