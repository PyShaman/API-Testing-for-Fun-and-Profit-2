import os
import pytest
import sys
import unittest

from assertpy import assert_that, soft_assertions
from requests.auth import HTTPBasicAuth

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods


@pytest.mark.client
class TestClientEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config = Config()
        cls.cm = CrudMethods()
        cls.url = config.URL
        cls.username = config.USR
        cls.password = config.PWD
        cls.api_key = cls.cm.request_method(
            "POST",
            cls.url,
            "/token",
            "",
            None,
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(cls.username, cls.password),
        ).json()["key"]

    def test_01_get_client_response_200(self):
        r = self.__class__().cm.request_method(
            "GET",
            self.url,
            "/clients",
            "",
            None,
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
            None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)

    def test_02_get_clients_invalid_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "GET",
            self.url,
            "/clients",
            "",
            None,
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"},
            None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_clients_none_api_key_response_403(self):
        r = self.__class__().cm.request_method(
            "GET",
            self.url,
            "/clients",
            "",
            None,
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")


if __name__ == "__main__":
    unittest.main()
