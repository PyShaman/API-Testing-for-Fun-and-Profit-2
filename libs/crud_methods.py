import backoff
import requests


class CrudMethods:
    @staticmethod
    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=3
    )
    def request_method(method, url, endpoint, client_id, headers, auth, data):
        return requests.request(
            method=method,
            url=f"{url}{endpoint}{client_id}",
            headers=headers,
            auth=auth,
            json=data,
        )

    def create(self, url, endpoint, client_id, headers, auth=None, data=None):
        return self.request_method(
            "POST", url, endpoint, client_id, headers, auth, data
        )

    def read(self, url, endpoint, client_id, headers, auth=None, data=None):
        return self.request_method("GET", url, endpoint, client_id, headers, auth, data)

    def update(self, url, endpoint, client_id, headers, auth=None, data=None):
        return self.request_method("PUT", url, endpoint, client_id, headers, auth, data)

    def delete(self, url, endpoint, client_id, headers, auth=None, data=None):
        return self.request_method(
            "DELETE", url, endpoint, client_id, headers, auth, data
        )
