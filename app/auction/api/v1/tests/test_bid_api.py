from common.tests.mixins import BaseAPIEndpointTestCase


class TestBidListAPIEndpoint(BaseAPIEndpointTestCase):
    url = "api:auction:v1:lots:bids"
    supported_methods = {"get", "post"}
