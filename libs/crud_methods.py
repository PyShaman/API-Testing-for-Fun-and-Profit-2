import backoff
import requests


class CrudMethods:
    @staticmethod
    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=10
    )
    def request_method(method, url, endpoint, client_id, headers, auth=None, data=None):
        return requests.request(
            method=method,
            url=f"{url}{endpoint}{client_id}",
            headers=headers,
            auth=auth,
            json=data,
        )


# Fun with decorators
class CrudMethodsWithDecorator:
    @staticmethod
    @backoff.on_exception(
        backoff.expo, requests.exceptions.RequestException, max_time=10
    )
    def request_method(method, url, endpoint, client_id, headers, auth=None, data=None):
        return requests.request(
            method=method,
            url=f"{url}{endpoint}{client_id}",
            headers=headers,
            auth=auth,
            json=data,
        )


# def post(func):
#     def wrapper():
#         print("Started")
#         func()
#         print("Ended")
#
#     return wrapper


def request_method(func):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        return val

    return wrapper


@request_method
def post(a):
    print(a)


def f1(func):
    def wrapper(*args, **kwargs):
        print("Started")
        func(*args, **kwargs)
        print("Ended")
    return wrapper


@f1
def f(a, b=9):
    print(a, b)
f("Hi")


post("POST", "self.config.URL", "/token", "", "{HttpHeaders.ACCEPT: 'application/json'}", "HTTPBasicAuth(self.config.USR, self.config.PWD))")
