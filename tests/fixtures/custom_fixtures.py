import pytest

from assertpy import assert_that
from http_constants.headers import HttpHeaders
from libs.client_data import ClientData
from libs.config import Config
from libs.crud_methods import CrudMethods
from requests.auth import HTTPBasicAuth


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def crud():
    return CrudMethods()


@pytest.fixture
def api_key(config, crud):
    return crud.create(
        config.URL,
        "/token",
        "",
        {HttpHeaders.ACCEPT: "application/json"},
        HTTPBasicAuth(config.USR, config.PWD),
    ).json()["key"]


@pytest.fixture
def client(config, crud, api_key):
    client_data = ClientData().return_client_data()
    _client = crud.create(
        config.URL,
        "/client",
        "",
        {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        data=client_data,
    )
    yield _client
    crud.delete(
        config.URL,
        "/client",
        f"/{_client.json()['id']}",
        {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
    )
    assert_that(
        crud.read(
            config.URL,
            "/client",
            f"/{_client.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        ).status_code
    ).is_equal_to(404)
