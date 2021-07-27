import backoff
import os
import pytest
import requests
import sys
import unittest

from assertpy import assert_that, soft_assertions
from requests.auth import HTTPBasicAuth

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods


@pytest.mark.auth
class TestTokenEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        config = Config()
        cls.cm = CrudMethods()
        cls.url = config.URL
        cls.username = config.USR
        cls.password = config.PWD
        print(cls.url)
        print(cls.username)
        print(cls.password)

    def test_01_get_api_key_response_200(self):
        r = self.__class__().cm.request_method("POST",
                                               self.__class__().url,
                                               "/token",
                                               "",
                                               None,
                                               {HttpHeaders.ACCEPT: "application/json"},
                                               HTTPBasicAuth(self.username, self.password))
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(r.json()["key"]).is_not_empty()

    def test_02_get_api_key_invalid_username_response_400(self):
        r = self.__class__().cm.request_method("POST",
                                               self.url,
                                               "/token",
                                               "",
                                               None,
                                               {HttpHeaders.ACCEPT: "application/json"},
                                               HTTPBasicAuth("invalid", self.password))
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")

    def test_03_get_api_key_invalid_password_response_400(self):
        r = self.__class__().cm.request_method("POST",
                                               self.url,
                                               "/token",
                                               "",
                                               None,
                                               {HttpHeaders.ACCEPT: "application/json"},
                                               HTTPBasicAuth(self.username, "invalid"))
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")


if __name__ == '__main__':
    unittest.main()
