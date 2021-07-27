import backoff
import requests


class CrudMethods:

    def __init__(self):
        pass

    @staticmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=10)
    def request_method(method, url, endpoint, client_id, json, headers, auth):
        return requests.request(method=method,
                                url=f"{url}{endpoint}{client_id}",
                                json=json,
                                headers=headers,
                                auth=auth)
