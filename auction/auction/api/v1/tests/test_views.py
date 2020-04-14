# Local
from common.tests.mixins import APIEndpointTestMixin, APITestMethodsGenerator


class TestMockView(APIEndpointTestMixin):
    url = "api:auction:v1:mock_view"
    supported_http_methods = {"get"}


APITestMethodsGenerator.generate_test_methods(TestMockView)
