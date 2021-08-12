import pytest

from assertpy import assert_that
from http_constants.headers import HttpHeaders
from libs.client_data import ClientData
from libs.config import Config
from libs.crud_methods import create_, read_, update_, delete_
from requests.auth import HTTPBasicAuth


@pytest.fixture
def config():
    return Config()


@pytest.fixture
def create():
    return create_


@pytest.fixture
def read():
    return read_


@pytest.fixture
def update():
    return update_


@pytest.fixture
def delete():
    return delete_


@pytest.fixture
def api_key(config, create):
    return create(
        f"{config.URL}/token",
        headers={HttpHeaders.ACCEPT: "application/json"},
        auth=HTTPBasicAuth(config.USR, config.PWD),
        json=None,
    ).json()["key"]


@pytest.fixture
def client(config, create, read, delete, api_key):
    client_data = ClientData().return_client_data()
    client_ = create(
        f"{config.URL}/client",
        headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        auth=None,
        json=client_data,
    )
    yield client_
    delete(
        f"{config.URL}/client/{client_.json()['id']}",
        headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        auth=None,
        json=None,
    )
    assert_that(
        read(
            f"{config.URL}/client/{client_.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        ).status_code
    ).is_equal_to(404)
