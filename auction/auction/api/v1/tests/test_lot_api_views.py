# Local
from freezegun import freeze_time
from rest_framework import status

from auction.api.v1.tests.factories import AuctionBidFactory, AuctionItemFactory
from auction.models import AuctionItem
from common.tests.factories import UserProfileFactory
from common.tests.mixins import (
    APITestMethodsGenerator,
    BaseAPIEndpointTestCase,
)


class TestLotListAPIEndpoint(BaseAPIEndpointTestCase):
    url = "api:auction:v1:lot_list_create"
    supported_methods = {"get", "post"}

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


class TestLotCreateAPIEndpoint(BaseAPIEndpointTestCase):
    url = "api:auction:v1:lot_list_create"
    supported_methods = {"get", "post"}

    def test_user_can_create_lot_with_minimal_information(self):
        self.assertEquals(AuctionItem.objects.count(), 0)
        create_data = {"name": "Old Portrait"}
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-18 04:35:01"):
            response = self.make_request(
                "post",
                HTTP_AUTHORIZATION=http_auth,
                data=create_data
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(AuctionItem.objects.count(), 1)
        item = AuctionItem.objects.get()
        expected_result = {
            "public_id": str(item.public_id),
            "created_at": "2020-04-18T04:35:01Z",
            "user": self.auth_user.user_profile.id,
            "name": "Old Portrait",
            "description": None,
            "base_price": "0.00",
            "base_price_currency": "GBP",
            "is_active": False
        }
        self.assertEqual(response.json(), expected_result)

    def test_user_can_create_lot_with_maximum_information(self):
        self.assertEquals(AuctionItem.objects.count(), 0)
        create_data = {
            "name": "Old Portrait",
            "description": "An old, dusty family portrait.",
            "base_price": "15.43",
            "base_price_currency": "EUR",
            "is_active": True
        }
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-18 04:35:01"):
            response = self.make_request(
                "post",
                HTTP_AUTHORIZATION=http_auth,
                data=create_data
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(AuctionItem.objects.count(), 1)
        item = AuctionItem.objects.get()
        expected_result = {
            "public_id": str(item.public_id),
            "created_at": "2020-04-18T04:35:01Z",
            "user": self.auth_user.user_profile.id,
            "name": "Old Portrait",
            "description": "An old, dusty family portrait.",
            "base_price": "15.43",
            "base_price_currency": "EUR",
            "is_active": True
        }
        self.assertEqual(response.json(), expected_result)

    def test_user_cannot_create_lot_missing_required_information(self):
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request("post", HTTP_AUTHORIZATION=http_auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"name": ["This field is required."]})


class TestLotRetrieveAPIEndpoint(BaseAPIEndpointTestCase):
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


class TestLotUpdateAPIEndpoint(BaseAPIEndpointTestCase):
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
        self.url_args = [self.auction_item.public_id]

    @property
    def partial_update_data(self):
        return {"is_active": False}

    @property
    def complete_update_data(self):
        return {
            "is_active": False,
            "base_price": "18.98",
            "base_price_currency": "EUR",
            "description": "Updated description.",
            "name": "Updated name",
        }

    def test_write_parameters_to_existing_auction_partial_update(self):
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-10 09:11:34"):
            response = self.make_request(
                "patch",
                HTTP_AUTHORIZATION=http_auth,
                data=self.partial_update_data,
                content_type="application/json"
            )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "base_price": "46.00",
            "base_price_currency": "GBP",
            "bids": [],
            "created_at": "2019-12-19T04:35:01Z",
            "description": "Beautiful antique that belonged to my granny.",
            "highest_bid": None,
            "is_active": False,
            "modified_at": "2020-04-10T09:11:34Z",
            "name": "Grandma's Music Box",
            "public_id": str(self.auction_item.public_id),
            "sale_record": None,
            "user": self.auth_user.user_profile.id
        }
        self.assertEquals(response.json(), expected_response)

        # Confirm that the table has added a modified_at record
        self.auction_item.refresh_from_db()
        self.assertEqual(
            self.auction_item.modified_at.strftime("%Y-%m-%d %H:%M:%s"),
            "2020-04-10 09:11:1586509894"
        )

    def test_write_parameters_to_existing_auction_complete_update(self):
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-10 09:11:34"):
            response = self.make_request(
                "put",
                HTTP_AUTHORIZATION=http_auth,
                data=self.complete_update_data,
                content_type="application/json"
            )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "base_price": "18.98",
            "base_price_currency": "EUR",
            "bids": [],
            "created_at": "2019-12-19T04:35:01Z",
            "description": "Updated description.",
            "highest_bid": None,
            "is_active": False,
            "modified_at": "2020-04-10T09:11:34Z",
            "name": "Updated name",
            "public_id": str(self.auction_item.public_id),
            "sale_record": None,
            "user": self.auth_user.user_profile.id
        }
        self.assertEquals(response.json(), expected_response)

        # Confirm that the table has added a modified_at record
        self.auction_item.refresh_from_db()
        self.assertEqual(
            self.auction_item.modified_at.strftime("%Y-%m-%d %H:%M:%s"),
            "2020-04-10 09:11:1586509894"
        )

    def test_read_only_parameters_to_auction_does_not_do_partial_update(self):
        read_only_parameters = {
            "created_at": "2012-01-31T00:00:00Z",
            "modified_at": "2020-04-10T09:11:34Z",
            "public_id": "2d9dca7f-e5a4-49ab-bb39-a44f296f0208",
            "user": 45
        }
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-10 09:11:34"):
            response = self.make_request(
                "patch",
                HTTP_AUTHORIZATION=http_auth,
                data=read_only_parameters,
                content_type="application/json"
            )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        expected_response = {
            "base_price": "46.00",
            "base_price_currency": "GBP",
            "bids": [],
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

        # Confirm that the table has added a modified_at record
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)

    def test_read_only_parameters_to_auction_bad_request(self):
        read_only_parameters = {
            "created_at": "2012-01-31T00:00:00Z",
            "modified_at": "2020-04-10T09:11:34Z",
            "public_id": "2d9dca7f-e5a4-49ab-bb39-a44f296f0208",
            "user": 45
        }
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time("2020-04-10 09:11:34"):
            response = self.make_request(
                "put",
                HTTP_AUTHORIZATION=http_auth,
                data=read_only_parameters,
                content_type="application/json"
            )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        expected_response = {"name": ["This field is required."]}
        self.assertEquals(response.json(), expected_response)

        # Confirm that the table has added a modified_at record
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)

    def test_authenticated_patch_request_to_invalid_auction_returns_404(self):
        non_existing_uuid = "048bee0f-659e-496f-85c4-7683f67b4525"
        # Confirm that the UUID is not in use as any auction item public id
        self.assertFalse(
            AuctionItem.objects.filter(public_id=non_existing_uuid).exists()
        )
        self.url_args = [non_existing_uuid]
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "patch",
            HTTP_AUTHORIZATION=http_auth,
            data=self.partial_update_data,
            content_type="application/json"
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.json(), {'detail': 'Not found.'})

        # Confirm that there was no modification in the database
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)

    def test_authenticated_put_request_to_invalid_auction_returns_404(self):
        non_existing_uuid = "048bee0f-659e-496f-85c4-7683f67b4525"
        # Confirm that the UUID is not in use as any auction item public id
        self.assertFalse(
            AuctionItem.objects.filter(public_id=non_existing_uuid).exists()
        )
        self.url_args = [non_existing_uuid]
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "put",
            HTTP_AUTHORIZATION=http_auth,
            data=self.complete_update_data,
            content_type="application/json"
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        # Confirm that there was no modification in the database
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)

    def test_authenticated_patch_request_to_deleted_auction_returns_404(self):
        self.auction_item.delete()
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "patch",
            HTTP_AUTHORIZATION=http_auth,
            data=self.partial_update_data,
            content_type="application/json"
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.json(), {'detail': 'Not found.'})

        # Confirm that there was no modification in the database
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)

    def test_authenticated_put_request_to_deleted_auction_returns_404(self):
        self.auction_item.delete()
        http_auth = self.get_http_authorization(self.auth_user)
        response = self.make_request(
            "put",
            HTTP_AUTHORIZATION=http_auth,
            data=self.complete_update_data,
            content_type="application/json"
        )
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.json(), {'detail': 'Not found.'})

        # Confirm that there was no modification in the database
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.modified_at)


class TestLotDeleteAPIEndpoint(BaseAPIEndpointTestCase):
    url = "api:auction:v1:lot_retrieve_update_destroy"
    supported_methods = {"get", "put", "patch", "delete"}

    def setUp(self):
        super().setUp()
        self.auction_item = AuctionItemFactory(user=self.auth_user.user_profile)
        self.url_args = [self.auction_item.public_id]

    def test_active_lot_cannot_be_deleted_with_endpoint(self):
        # Set the auction item active
        self.auction_item.is_active = True
        self.auction_item.save()

        # Make request and confirm expected response and status code
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time(f"2020-02-10 10:00:00"):
            response = self.make_request("delete", HTTP_AUTHORIZATION=http_auth)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {
                'detail': (
                    'Cannot delete a lot which is currently active. '
                    'Please set it inactive first.'
                )
            }
        )

        # Confirm that the item has NOT been deleted from the database
        self.assertQuerysetEqual(
            AuctionItem.objects.all(),
            [repr(self.auction_item)]
        )
        self.auction_item.refresh_from_db()
        self.assertIsNone(self.auction_item.deleted_at)

    def test_inactive_lot_is_successfully_soft_deleted(self):
        # Set the auction item inactive
        self.auction_item.is_active = False
        self.auction_item.save()

        # Make request and confirm expected response and status code
        http_auth = self.get_http_authorization(self.auth_user)
        with freeze_time(f"2020-02-10 10:00:00"):
            response = self.make_request("delete", HTTP_AUTHORIZATION=http_auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content.decode("utf-8"), "")

        # Confirm that the item has been deleted from the database
        self.assertQuerysetEqual(AuctionItem.objects.all(), [])
        self.auction_item.refresh_from_db()
        self.assertEqual(
            self.auction_item.deleted_at.strftime("%Y-%m-%d %H:%M:%s"),
            "2020-02-10 10:00:1581328800"
        )


APITestMethodsGenerator.generate_test_methods(TestLotListAPIEndpoint)
APITestMethodsGenerator.generate_test_methods(TestLotCreateAPIEndpoint)
APITestMethodsGenerator.generate_test_methods(TestLotRetrieveAPIEndpoint)
APITestMethodsGenerator.generate_test_methods(TestLotUpdateAPIEndpoint)
APITestMethodsGenerator.generate_test_methods(TestLotDeleteAPIEndpoint)
