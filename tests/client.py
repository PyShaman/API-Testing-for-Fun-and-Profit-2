import pytest
import unittest

from assertpy import assert_that, soft_assertions
from requests.auth import HTTPBasicAuth

from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods


@pytest.mark.client
class TestClientEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = Config()
        cls.cm = CrudMethods()
        cls.api_key = cls.cm.create(
            cls.config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(cls.config.USR, cls.config.PWD),
        ).json()["key"]

    def test_01_get_client_response_200(self):
        r = self.__class__().cm.read(
            self.config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": self.api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)

    def test_02_get_clients_invalid_api_key_response_403(self):
        r = self.__class__().cm.read(
            self.config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_clients_none_api_key_response_403(self):
        r = self.__class__().cm.read(
            self.config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")
