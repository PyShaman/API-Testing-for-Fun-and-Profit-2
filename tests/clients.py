import pytest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders


@pytest.mark.clients
class TestClientsEndpoint:
    def test_01_get_clients_response_200(self, config, crud, api_key):
        r = crud.read(
            config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)

    def test_02_get_clients_invalid_api_key_response_403(self, config, crud):
        r = crud.read(
            config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid_api_key"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_clients_none_api_key_response_403(self, config, crud):
        r = crud.read(
            config.URL,
            "/clients",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(403)
            assert_that(r.json()["message"]).is_equal_to("invalid or missing api key")
