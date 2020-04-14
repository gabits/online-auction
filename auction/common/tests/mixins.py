# Python standard
import urllib
from typing import Callable

# Django
from django.test import TestCase
from django.urls import reverse

# Third-party
from rest_framework import status

# Local
from common.tests.factories import UserFactory


class APITestMethodsGenerator:
    """
    API test cases method generator.

    Generates useful test methods for API endpoints which follow a
    pre-defined structure (see APIEndpointTestMixin).

    To benefit from it, call the class method `generate_test_methods` providing
    it the class you want to extend test methods coverage for, as per the
    example below.

    Usage:

        >>> class MyTestCase(TestCase):
        >>>     ...
        >>>
        >>> APITestMethodsGenerator.generate_test_methods(MyTestCase)

    """
    # Supported HTTP methods by Django Rest Framework endpoints
    HTTP_METHODS = {"get", "patch", "post", "put", "delete", "head", "options"}

    @staticmethod
    def add_test_scenario(klass, test_scenario):
        setattr(klass, test_scenario.__name__, test_scenario)

    @classmethod
    def generate_test_methods(cls, klass):
        """
        Generate multiple test methods for a given class to increase test
        coverage of endpoints.
        """
        cls.generate_methods_for_unauthenticated_user_request(klass)
        cls.generate_methods_for_http_methods_not_allowed(klass)

    @classmethod
    def generate_methods_for_unauthenticated_user_request(cls, klass):
        for http_method in cls.HTTP_METHODS:
            test_scenario = cls.unauthenticated_method_test_factory(http_method)
            cls.add_test_scenario(klass, test_scenario)

    @classmethod
    def generate_methods_for_http_methods_not_allowed(cls, klass):
        methods_not_allowed = cls.HTTP_METHODS.difference(
            klass.supported_http_methods
        )
        for http_method in methods_not_allowed:
            test_scenario = cls.not_allowed_method_test_factory(http_method)
            cls.add_test_scenario(klass, test_scenario)

    @staticmethod
    def unauthenticated_method_test_factory(http_method: str) -> Callable:
        """
        Generates a function to test an unauthenticated request for a given
        HTTP request method, named accordingly.
        """
        def _unauthenticated_method_test(self):
            self.authenticate()
            response = self.make_request(http_method)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(
                bytes.decode(response.rendered_content, "utf-8"),
                '{"detail":"Authentication credentials were not provided."}'
            )

        test_method = _unauthenticated_method_test
        test_method.__name__ = (
            f'test_unauthenticated_{http_method}_request_returns_403_forbidden'
        )
        return test_method

    @staticmethod
    def not_allowed_method_test_factory(http_method: str) -> Callable:
        """
        Generates a function to test an unauthenticated request for a given
        HTTP request method, named accordingly.
        """
        def _not_allowed_method_test(self):
            response = self.make_request(http_method)
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
            self.assertEqual(
                bytes.decode(response.rendered_content, "utf-8"),
                "{'detail': f'Method \"{method.upper()}\" not allowed.'}"
            )

        test_method = _not_allowed_method_test
        test_method.__name__ = (
            f'test_{http_method}_request_returns_405_not_allowed'
        )
        return test_method


class APIEndpointTestMixin(APITestMethodsGenerator, TestCase):
    """
    Mixin class to help testing a single API endpoint.

    Must be used in combination with Django's TestCase.

    Usage:

        >>> class MyTest(APIEndpointTestMixin, TestCase):
        >>>     url = 'app_name:endpoint_url'
        >>>     methods = {"get", "post"}

    """
    # Extend amount of debug information, provided by `unittest.TestCase`
    longMessage = True
    # HTTP methods supported by the endpoint
    supported_http_methods: set
    # Name spaced internal URL name to be tested by extending class
    url: str
    # Args and kwargs to provide the URL so it can successfully reverse it
    url_args: list = []
    url_kwargs: dict = {}

    @property
    def allowed_methods(self) -> set:
        return self.supported_http_methods.union({"head", "options"})

    def _get_url(self, query_params: str = None):
        url = reverse(self.url, args=self.url_args, kwargs=self.url_kwargs)
        if query_params:
            encoded_params = urllib.parse.urlencode(query_params)
            url += f"?{encoded_params}"
        return url

    def make_request(self, method: str, *args, **kwargs):
        query_params = kwargs.pop("query_params", None)
        url = self._get_url(query_params=query_params)
        client_method = getattr(self.client, method)
        return client_method(url, *args, **kwargs)

    def setUp(self):
        self.user = UserFactory()

    def authenticate(self):
        self.client.force_login(self.user)
