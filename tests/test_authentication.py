import backoff
import os
import requests
import sys
import unittest

from requests.auth import HTTPBasicAuth

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods


class TestBasicAuth(unittest.TestCase):

    def setUpClass(cls) -> None:
        config = Config()
        cls.cm = CrudMethods()
        cls.url = config.URL
        cls.username = config.USERNAME
        cls.password = config.PASSWORD

    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
    def test_get_api_key_response_200(self):
        r = self.__class__().cm.request_method("POST",
                                   self.url,
                                   "/token",
                                   None,
                                   {HttpHeaders.ACCEPT: "application/json"},
                                   HTTPBasicAuth(self.username, self.password))
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(r.json()["key"]).is_not_empty()
        print(r.json()["key"])


if __name__ == '__main__':
    unittest.main()
