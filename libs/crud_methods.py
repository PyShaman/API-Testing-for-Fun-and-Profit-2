import backoff
import requests

from functools import partial


class CrudMethods:
    @staticmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=3)
    def request_method(url, endpoint, client_id, headers, auth, data, method):
        return requests.request(
            method=method,
            url=f"{url}{endpoint}{client_id}",
            headers=headers,
            auth=auth,
            json=data,
        )

    def create(self, url, endpoint, client_id, headers, auth=None, data=None):
        req = partial(self.request_method, method="POST")
        return req(url, endpoint, client_id, headers, auth, data)

    def read(self, url, endpoint, client_id, headers, auth=None, data=None):
        req = partial(self.request_method, method="GET")
        return req(url, endpoint, client_id, headers, auth, data)

    def update(self, url, endpoint, client_id, headers, auth=None, data=None):
        req = partial(self.request_method, method="PUT")
        return req(url, endpoint, client_id, headers, auth, data)

    def delete(self, url, endpoint, client_id, headers, auth=None, data=None):
        req = partial(self.request_method, method="DELETE")
        return req(url, endpoint, client_id, headers, auth, data)
