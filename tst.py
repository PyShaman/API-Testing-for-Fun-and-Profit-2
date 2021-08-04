import requests
from functools import partial


def http(crud):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(crud, *args, **kwargs)
        return wrapper
    return decorator


@http("GET")
def req(method, url, endpoint, ):
    return requests.request("aaaa", "clients", "", {"accept": "application/json", "X-API-KEY": "invalid_api_key"})


print(req())
