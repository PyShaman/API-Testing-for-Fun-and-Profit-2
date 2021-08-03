import pytest
import unittest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth

from libs.client_data import ClientData
from libs.config import Config
from libs.crud_methods import CrudMethods


@pytest.mark.clients
class TestClientsEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = Config()
        cd = ClientData()
        cls.client_data = cd.return_client_data()
        cls.cleanup = []
        cls.cm = CrudMethods()
        cls.api_key = cls.cm.request_method(
            "POST",
            cls.config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(cls.config.USR, cls.config.PWD),
        ).json()["key"]

    @classmethod
    def tearDownClass(cls) -> None:
        for client_id in cls.cleanup:
            cls.cm.request_method(
                "DELETE",
                cls.config.URL,
                "/client",
                f"/{client_id}",
                {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": cls.api_key},
            )
            assert_that(
                cls.cm.request_method(
                    "GET",
                    cls.config.URL,
                    "/client",
                    f"/{client_id}",
                    {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": cls.api_key},
                ).status_code
            ).is_equal_to(404)

    def test_01_get_client_response_200(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "GET",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()).is_equal_to(re.json())

    def test_02_get_client_invalid_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "GET",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_client_missing_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "GET",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_04_get_client_not_existing(self):
        r = self.__class__().cm.request_method(
            "GET",
            self.config.URL,
            "/client",
            "/123",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_05_put_client_response_200(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()["id"]).is_equal_to(re.json()["id"])
            assert_that(r.json()).is_equal_to(re.json())

    def test_06_put_client_response_invalid_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("invalid request")

    def test_07_put_client_response_without_first_name_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={"lastName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("firstName is required")

    def test_08_put_client_response_without_last_name_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={"firstName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("lastName is required")

    def test_09_put_client_response_without_phone_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={"firstName": "Aldona", "lastName": "Boruta"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("phone is required")

    def test_10_put_client_invalid_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
            data={"lastName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_11_put_client_empty_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "PUT",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            data={"lastName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_12_delete_client_response_200(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        re = self.__class__().cm.request_method(
            "DELETE",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_13_delete_client_invalid_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "DELETE",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_14_delete_client_empty_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data,
        )
        self.__class__().cleanup.append(r.json()["id"])
        re = self.__class__().cm.request_method(
            "DELETE",
            self.config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_14_delete_client_response_404(self):
        r = self.__class__().cm.request_method(
            "DELETE",
            self.config.URL,
            "/client",
            f"/777",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_15_verify_length_first_name(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={
                "firstName": "a" * 51,
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        self.__class__().cleanup.append(r.json()["id"])
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["firstName"])).is_equal_to(50)

    def test_16_verify_length_last_name(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={
                "firstName": "Boruta",
                "lastName": "Boruta" * 20,
                "phone": "+48 22 632 1512",
            },
        )
        self.__class__().cleanup.append(r.json()["id"])
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["lastName"])).is_equal_to(50)

    def test_17_verify_length_last_name(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data={"firstName": "Boruta", "lastName": "Boruta", "phone": "123" * 200},
        )
        self.__class__().cleanup.append(r.json()["id"])
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["phone"])).is_equal_to(50)

    def test_18_verify_bad_request_returns_500(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            data=self.client_data.pop("firstName"),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(500)
