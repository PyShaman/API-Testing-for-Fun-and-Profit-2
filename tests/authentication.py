import pytest
import unittest

from assertpy import assert_that, soft_assertions
from requests.auth import HTTPBasicAuth

from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods


@pytest.mark.auth
class TestTokenEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = Config()
        cls.cm = CrudMethods()

    def test_01_get_api_key_response_200(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(self.config.USR, self.config.PWD),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(r.json()["key"]).is_not_empty()

    def test_02_get_api_key_invalid_username_response_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth("invalid", self.config.PWD),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")

    def test_03_get_api_key_invalid_password_response_400(self):
        r = self.__class__().cm.request_method(
            "POST",
            self.config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(self.config.USR, "invalid"),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")
