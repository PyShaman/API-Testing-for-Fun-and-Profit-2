import pytest

from assertpy import assert_that, soft_assertions
from http_constants.headers import HttpHeaders
from libs.client_data import ClientData


@pytest.mark.client
class TestClientEndpoint:
    def test_01_get_client_response_200(self, config, read, api_key, client):
        r = client
        re = read(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()).is_equal_to(re.json())

    def test_02_get_client_invalid_api_key_response_403(self, config, read, client):
        r = client
        re = read(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_03_get_client_missing_api_key_response_403(self, config, read, client):
        r = client
        re = read(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_04_get_client_not_existing(self, read, config, api_key):
        r = read(
            f"{config.URL}/client/123",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_05_put_client_response_200(self, config, update, api_key, client):
        client_data = ClientData().return_client_data()
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=client_data,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(r.json()["id"]).is_equal_to(re.json()["id"])
            assert_that(r.json()).is_equal_to(re.json())

    def test_06_put_client_response_invalid_400(self, config, update, api_key, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("invalid request")

    def test_07_put_client_response_without_first_name_400(self, config, update, api_key, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={"lastName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("firstName is required")

    def test_08_put_client_response_without_last_name_400(self, config, update, api_key, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={"firstName": "Boruta", "phone": "+48 22 632 1512"},
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("lastName is required")

    def test_09_put_client_response_without_phone_400(self, config, update, api_key, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={
                "firstName": "Aldona", 
                "lastName": "Boruta"
            },
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(400)
            assert_that(re.json()["message"]).is_equal_to("phone is required")

    def test_10_put_client_invalid_api_key_response_403(self, config, update, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
            auth=None,
            json={
                "firstName": "Aldona",
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_11_put_client_empty_api_key_response_403(self, config, update, client):
        r = client
        re = update(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            auth=None,
            json={
                "firstName": "Aldona",
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_12_delete_client_response_200(self, config, delete, api_key, client):
        r = client
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_13_delete_client_invalid_api_key_response_403(self, config, delete, client):
        r = client
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": "invalid"},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_14_delete_client_empty_api_key_response_403(self, config, delete, client):
        r = client
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": None},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(re.status_code).is_equal_to(403)
            assert_that(re.json()["message"]).is_equal_to("invalid or missing api key")

    def test_15_delete_client_response_404(self, config, delete, api_key):
        r = delete(
            f"{config.URL}/client/777",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(404)
            assert_that(r.json()["message"]).is_equal_to("client not found")

    def test_16_verify_length_first_name(self, config, create, delete, api_key):
        r = create(
            f"{config.URL}/client",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={
                "firstName": "a" * 51,
                "lastName": "Boruta",
                "phone": "+48 22 632 1512",
            },
        )
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["firstName"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_17_verify_length_last_name(self, config, create, delete, api_key):
        r = create(
            f"{config.URL}/client",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={
                "firstName": "Boruta",
                "lastName": "a" * 51,
                "phone": "+48 22 632 1512",
            },
        )
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["lastName"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_18_verify_length_phone(self, config, create, delete, api_key):
        r = create(
            f"{config.URL}/client",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json={
                "firstName": "Boruta", 
                "lastName": "Boruta", 
                "phone": "1" * 51},
        )
        re = delete(
            f"{config.URL}/client/{r.json()['id']}",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=None,
        )
        with soft_assertions():
            assert_that(r.status_code).is_equal_to(200)
            assert_that(len(r.json()["phone"])).is_equal_to(50)
            assert_that(re.status_code).is_equal_to(200)
            assert_that(re.json()["message"]).is_equal_to("client deleted")

    def test_19_verify_bad_request_returns_500(self, config, create, api_key):
        client_data = ClientData().return_client_data()
        r = create(
            f"{config.URL}/client",
            headers={HttpHeaders.ACCEPT: "application/json", "X-API-KEY": api_key},
            auth=None,
            json=client_data.pop("firstName"),
        )
        assert_that(r.status_code).is_equal_to(500)
