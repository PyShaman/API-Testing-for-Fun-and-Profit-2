import pytest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth


@pytest.mark.auth
class TestTokenEndpoint:
    def test_01_get_api_key_response_200(self, config, create):
        r = create(
            f"{config.URL}/token",
            headers={HttpHeaders.ACCEPT: "application/json"},
            auth=HTTPBasicAuth(config.USR, config.PWD),
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(r.json()["key"]).is_not_empty()

    def test_02_get_api_key_invalid_username_response_400(self, config, create):
        r = create(
            f"{config.URL}/token",
            headers={HttpHeaders.ACCEPT: "application/json"},
            auth=HTTPBasicAuth("invalid", config.PWD),
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")

    def test_03_get_api_key_invalid_password_response_400(self, config, create):
        r = create(
            f"{config.URL}/token",
            headers={HttpHeaders.ACCEPT: "application/json"},
            auth=HTTPBasicAuth(config.USR, "invalid"),
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")
