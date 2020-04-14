# Local
from common.tests.mixins import APIEndpointTestMixin, APITestMethodsGenerator


class TestMockView(APIEndpointTestMixin):
    url = "api:auction:v1:mock_view"
    endpoint_methods = {"get"}


APITestMethodsGenerator.generate_test_methods(TestMockView)
