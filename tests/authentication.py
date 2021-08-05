import pytest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from libs.config import Config
from libs.crud_methods import CrudMethods
from requests.auth import HTTPBasicAuth


@pytest.fixture
def config():
    _config = Config()
    return _config


@pytest.fixture
def crud():
    cm = CrudMethods()
    return cm


@pytest.mark.auth
class TestTokenEndpoint:
    def test_01_get_api_key_response_200(self, config, crud):
        r = crud.create(
            config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(config.USR, config.PWD),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(r.json()["key"]).is_not_empty()

    def test_02_get_api_key_invalid_username_response_400(self, config, crud):
        r = crud.create(
            config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth("invalid", config.PWD),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")

    def test_03_get_api_key_invalid_password_response_400(self, config, crud):
        r = crud.create(
            config.URL,
            "/token",
            "",
            {HttpHeaders.ACCEPT: "application/json"},
            HTTPBasicAuth(config.USR, "invalid"),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(400)
            assert_that(r.json()["message"]).is_equal_to("invalid username or password")
