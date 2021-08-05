import pytest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from libs.client_data import ClientData
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


@pytest.fixture
def api_key(config, crud):
    key = crud.create(
        config.URL,
        "/token",
        "",
        {HttpHeaders.ACCEPT: "application/json"},
        HTTPBasicAuth(config.USR, config.PWD),
    ).json()["key"]
    return key


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


@pytest.mark.client
class TestClientEndpoint:
    def test_01_get_client_response_200(self, config, crud, api_key, client):
        r = client
        re = crud.read(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()).is_equal_to(re.json())

    def test_02_get_client_invalid_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.read(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_client_missing_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.read(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_04_get_client_not_existing(self, crud, config, api_key):
        r = crud.read(
            config.URL,
            "/client",
            "/123",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_05_put_client_response_200(self, config, crud, api_key, client):
        client_data = ClientData().return_client_data()
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data=client_data,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()["id"]).is_equal_to(re.json()["id"])
            assert_that(r.json()).is_equal_to(re.json())

    def test_06_put_client_response_invalid_400(self, config, crud, api_key, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("invalid request")

    def test_07_put_client_response_without_first_name_400(self, config, crud, api_key, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={"lastName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("firstName is required")

    def test_08_put_client_response_without_last_name_400(self, config, crud, api_key, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={"firstName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("lastName is required")

    def test_09_put_client_response_without_phone_400(self, config, crud, api_key, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={"firstName": "Aldona", "lastName": "Boruta"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("phone is required")

    def test_10_put_client_invalid_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
            data={
                "firstName": "Aldona",
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_11_put_client_empty_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.update(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            data={
                "firstName": "Aldona",
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_12_delete_client_response_200(self, config, crud, api_key, client):
        r = client
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_13_delete_client_invalid_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_14_delete_client_empty_api_key_response_403(self, config, crud, client):
        r = client
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_15_delete_client_response_404(self, config, crud, api_key):
        r = crud.delete(
            config.URL,
            "/client",
            f"/777",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_16_verify_length_first_name(self, config, crud, api_key):
        r = crud.create(
            config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={
                "firstName": "a" * 51,
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["firstName"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_17_verify_length_last_name(self, config, crud, api_key):
        r = crud.create(
            config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={
                "firstName": "Boruta",
                "lastName": "a" * 51,
                "phone": "+48 22 632 1512",
            },
        )
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["lastName"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_18_verify_length_phone(self, config, crud, api_key):
        r = crud.create(
            config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data={"firstName": "Boruta", "lastName": "Boruta", "phone": "1" * 51},
        )
        re = crud.delete(
            config.URL,
            "/client",
            f"/{r.json()['id']}",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["phone"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_19_verify_bad_request_returns_500(self, config, crud, api_key):
        client_data = ClientData().return_client_data()
        r = crud.create(
            config.URL,
            "/client",
            "",
            {HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            data=client_data.pop("firstName"),
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(500)
