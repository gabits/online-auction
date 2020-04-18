# Local
from freezegun import freeze_time
from rest_framework import status

from auction.api.v1.tests.factories import AuctionBidFactory, AuctionItemFactory
from auction.models import AuctionItem
from common.tests.factories import UserProfileFactory
from common.tests.mixins import APIEndpointTestMixin, APITestMethodsGenerator


class TestLotListAPIEndpoint(APIEndpointTestMixin):
    url = "api:auction:v1:lot_list_create"
    supported_methods = {"get", "post"}
    maxDiff = None

    def setUp(self):
        """
        Set up a few auction items, each created by a different user,
        with different attributes such as name and description, and test that
        they are returned by the API as the expected formats and with
        accurate data (reflecting the database).
        """
        uuid_list = [
            "835d0415-4a38-4f53-bb15-1339b4d825ba",
            "16727ef1-d110-4c3b-8b2e-24b3395fedd4",
            "e8f757a3-2fb1-4275-8473-729edc8ced4a",

        ]
        super().setUp()
        for n in range(1, 4):
            # Create auction items with different created_at times so we can
            # have a production-like scenario
            setattr(
                self,
                f"user_profile_{n}",
                UserProfileFactory()
            )
            with freeze_time(f"2019-12-19 0{n}:35:01"):
                setattr(
                    self,
                    f"auction_item_{n}",
                    AuctionItemFactory(
                        user=getattr(self, f"user_profile_{n}"),
                        name=f"Name {n}",
                        base_price=str(53.51 + n),
                        description=f"Description {n}",
                        # Create active and inactive items
                        is_active=bool(n % 2),
                        public_id=uuid_list[n - 1]
                    )
                )

    def get_expected_lots(self) -> tuple:
        lot_1 = {
            "public_id": "835d0415-4a38-4f53-bb15-1339b4d825ba",
            "created_at": "2019-12-19T01:35:01Z",
            "user": 2,
            "name": "Name 1",
            "description": "Description 1",
            "base_price": "54.51",
            "base_price_currency": "GBP",
            "is_active": True
        }
        lot_2 = {
            "public_id": "16727ef1-d110-4c3b-8b2e-24b3395fedd4",
            "created_at": "2019-12-19T02:35:01Z",
            "user": 3,
            "name": "Name 2",
            "description": "Description 2",
            "base_price": "55.51",
            "base_price_currency": "GBP",
            "is_active": False
        }
        lot_3 = {
            "public_id": "e8f757a3-2fb1-4275-8473-729edc8ced4a",
            "created_at": "2019-12-19T03:35:01Z",
            "user": 4,
            "name": "Name 3",
            "description": "Description 3",
            "base_price": "56.51",
            "base_price_currency": "GBP",
            "is_active": True
        }
        return lot_1, lot_2, lot_3

    def test_authenticated_get_request_when_no_auctions_returns_empty(self):
        AuctionItem.objects.delete()
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("get", HTTP_AUTHORIZATION=http_auth)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_returns_existing_auctions(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("get", HTTP_AUTHORIZATION=http_auth)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        lot_1, lot_2, lot_3 = self.get_expected_lots()
        expected_response = {
            # Confirm results are paginated
            "count": 3,
            "next": None,
            "previous": None,
            "results": [lot_1, lot_2, lot_3]
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_can_filter_active_lots(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "get",
            HTTP_AUTHORIZATION=http_auth,
            query_params={"is_active": True}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        lot_1, _, lot_3 = self.get_expected_lots()
        expected_response = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [lot_1, lot_3]
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_can_filter_inactive_lots(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "get",
            HTTP_AUTHORIZATION=http_auth,
            query_params={"is_active": False}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        _, lot_2, _ = self.get_expected_lots()
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [lot_2]
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_can_order_lots_by_created_time(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "get",
            HTTP_AUTHORIZATION=http_auth,
            query_params={"ordering": "-created_at"}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        lot_1, lot_2, lot_3 = self.get_expected_lots()
        expected_response = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [lot_3, lot_2, lot_1]
        }
        self.assertEquals(response.json(), expected_response)

    def test_authenticated_get_request_can_search_by_name(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "get",
            HTTP_AUTHORIZATION=http_auth,
            query_params={"search": "Name 3"}
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        _, _, lot_3 = self.get_expected_lots()
        expected_response = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [lot_3]
        }
        self.assertEquals(response.json(), expected_response)


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


APITestMethodsGenerator.generate_test_methods(TestLotListAPIEndpoint)
APITestMethodsGenerator.generate_test_methods(TestLotRetrieveAPIEndpoint)
