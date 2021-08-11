import requests
from requests.auth import HTTPBasicAuth


def request_method(method):
    def decorator(response):
        def wrapper(*args, **kwargs):
            return requests.request(method, *args, **kwargs)

        return wrapper

    return decorator


@request_method("POST")
def create_(self, url, headers, auth, json, timeout=7):
    pass


@request_method("GET")
def read_(self, url, headers, auth, json, timeout=7):
    pass


@request_method("PUT")
def update_(self, url, headers, auth, json, timeout=7):
    pass


@request_method("DELETE")
def delete_(self, url, headers, auth, json, timeout=7):
    pass


print(create_("https://qa-interview-api.migo.money/token", headers={"accept": "application/json"}, auth=HTTPBasicAuth("egg", "f00BarbAz!"), json=None).status_code)
