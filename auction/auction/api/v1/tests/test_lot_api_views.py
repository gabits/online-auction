# Local
from freezegun import freeze_time
from rest_framework import status

from auction.api.v1.tests.factories import AuctionBidFactory, AuctionItemFactory
from auction.models import AuctionItem
from common.tests.mixins import APIEndpointTestMixin, APITestMethodsGenerator


class TestLotRetrieveAPIEndpoint(APIEndpointTestMixin):
    url = "api:auction:v1:lot_retrieve_update_destroy"
    supported_methods = {"get", "put", "patch", "delete"}

    def setUp(self):
        super().setUp()
        with freeze_time("2019-12-19 04:35:01"):
            self.auction_item = AuctionItemFactory(
                user=self.auth_user.user_profile,
                base_price="46.00",
                name="Grandma's Music Box",
                description="Beautiful antique that belonged to my granny.",
                is_active=True
            )
        for n in range(1, 4):
            setattr(
                self,
                f"bid_{n}",
                AuctionBidFactory(item=self.auction_item)
            )
        self.url_args = [self.auction_item.public_id]

    def test_authenticated_get_request_to_existing_auction_returns_200(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("get", HTTP_AUTHORIZATION=http_auth)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "base_price": "46.00",
            "base_price_currency": "GBP",
            # TODO: change this; add endpoint to retrieve bids
            "bids": [
                self.bid_3.id,
                self.bid_2.id,
                self.bid_1.id,
            ],
            "created_at": "2019-12-19T04:35:01Z",
            "description": "Beautiful antique that belonged to my granny.",
            "highest_bid": None,
            "is_active": True,
            "modified_at": None,
            "name": "Grandma's Music Box",
            "public_id": str(self.auction_item.public_id),
            "sale_record": None,
            "user": self.auth_user.user_profile.id
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_to_invalid_auction_returns_404(self):
        non_existing_uuid = "048bee0f-659e-496f-85c4-7683f67b4525"
        # Confirm that the UUID is not in use as any auction item public id
        self.assertFalse(
            AuctionItem.objects.filter(public_id=non_existing_uuid).exists()
        )
        self.url_args = [non_existing_uuid]
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("get", HTTP_AUTHORIZATION=http_auth)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.json(), {'detail': 'Not found.'})

    def test_authenticated_get_request_to_deleted_auction_returns_404(self):
        self.auction_item.delete()
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("get", HTTP_AUTHORIZATION=http_auth)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.json(), {'detail': 'Not found.'})


APITestMethodsGenerator.generate_test_methods(TestLotRetrieveAPIEndpoint)
