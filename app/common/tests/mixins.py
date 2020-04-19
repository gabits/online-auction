# Python standard
import urllib
from datetime import timedelta
from typing import Callable

# Django
from django.conf import settings
from django.conf.global_settings import AUTH_USER_MODEL
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# Third-party
from oauth2_provider.models import AccessToken
from requests import Response
from rest_framework import status

# Local
from account.tests.factories import AuthUserFactory


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
        """
        Attach the generated test function to the test class so it is ran
        when tests are executed.
        """
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
        """
        Create and attach test methods for HTTP requests which do not provide
        authorization credentials, using all HTTP methods - both supported and
        unsupported by the endpoint.
        """
        for http_method in cls.HTTP_METHODS:
            test_scenario = cls.unauthenticated_method_test_factory(http_method)
            cls.add_test_scenario(klass, test_scenario)

    @classmethod
    def generate_methods_for_http_methods_not_allowed(cls, klass):
        """
        Create and attach test methods for each HTTP request using methods not
        supported by the endpoint being tested.
        """
        methods_not_allowed = cls.HTTP_METHODS.difference(
            klass.get_supported_http_methods()
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
            response = self.make_request(http_method)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
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
            http_auth = self.get_http_authorization()
            response = self.make_request(
                http_method,
                HTTP_AUTHORIZATION=http_auth
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_405_METHOD_NOT_ALLOWED
            )
            self.assertEqual(
                bytes.decode(response.rendered_content, "utf-8"),
                f'{{"detail":"Method \\\"{http_method.upper()}\\\" '
                f'not allowed.\"}}'
            )

        test_method = _not_allowed_method_test
        test_method.__name__ = (
            f'test_{http_method}_request_returns_405_not_allowed'
        )
        return test_method


class BaseAPIEndpointTestCase(APITestMethodsGenerator, TestCase):
    """
    Mixin class to help testing a single API endpoint.

    Inheriting from this class will create additional test methods for the
    test case, based on the configuration provided with the test attributes.

    The extended test scenarios will check for unauthorized requests and HTTP
    requests using methods not allowed.

    Public methods:
    . `get_http_authorization`: provide request header authorization credentials
    . `setUp`: set up method to be ran once for each individual test method
    . `make_request`: utility method to simplify requests to specified endpoint

    Usage:

        >>> class MyTest(BaseAPIEndpointTestCase):
        >>>     url = 'app_name:endpoint_url'
        >>>     supported_methods = {"get", "post"}

    """
    # Extend amount of debug information, provided by `unittest.TestCase`
    longMessage = True
    maxDiff = None
    # HTTP methods supported by the endpoint
    supported_methods: set
    # Name spaced internal URL name to be tested by extending class
    url: str
    # Args and kwargs to provide the URL so it can successfully reverse it
    url_args: list = []
    url_kwargs: dict = {}

    @classmethod
    def get_supported_http_methods(cls) -> set:
        """
        Get all HTTP methods which the specified endpoint supports.
        """
        return cls.supported_methods.union({"head", "options"})

    def _get_url(self, query_params: str = None) -> str:
        """
        Get the absolute URL path, including domain, path and encoded
        parameters.
        """
        url = reverse(self.url, args=self.url_args, kwargs=self.url_kwargs)
        if query_params:
            encoded_params = urllib.parse.urlencode(query_params)
            url += f"?{encoded_params}"
        return url

    def make_request(
        self,
        method: str,
        *args,
        query_params: dict = None,
        **kwargs
    ) -> Response:
        """
        Make a request to any specified HTTP method.

        Can be provided any parameters supported by the `requests` library,
        which is responsible for executing these requests.

        Also supports receiving a `query_params` dictionary, which it encodes
        in the URL before making the request, to facilitate testing URL query
        parameters.
        """
        url = self._get_url(query_params=query_params)
        client_method = getattr(self.client, method)
        return client_method(url, *args, **kwargs)

    def setUp(self):
        super().setUp()
        self.auth_user = AuthUserFactory()

    def get_http_authorization(self, user: AUTH_USER_MODEL = None) -> str:
        """
        Get full OAuth 2.0 token credentials for HTTP_AUTHORIZATION header in
        order to make a request for the specified user only.

        The credentials generated expire after 5 minutes. This method is for
        testing purposes only.
        """
        if not user:
            user = self.auth_user
        access_token = AccessToken.objects.create(
            user=user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
        )
        return f"{settings.OAUTH2_AUTHORIZATION_SCHEME} {access_token}"
