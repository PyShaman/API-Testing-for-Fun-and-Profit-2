import requests


def http(*crud):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("*crud", *crud, type(*crud))
            print("*args", *args)
            print("**kwarg", **kwargs)
            return func(*crud, *args, **kwargs)
        return wrapper
    return decorator


@http("GET")
def request_method(url, endpoint, client_id, headers, authorization=None, payload=None):
    return requests.request(f"{url}{endpoint}{client_id}", headers, auth=authorization, data=payload)


print(request_method("smth",
                     "clients",
                     "",
                     {"accept": "application/json", "X-API-KEY": "invalid_api_key"}))

# def rest_method(*args, **kwargs):
#     def decorator(func):
#         def wrapper(url, endpoint, client_id, headers, kwargs["method"], auth=None, data=None):
#             return func(url, endpoint, client_id, headers, argument=argument, auth=auth, data=data)
#         return wrapper
#     return decorator
#
#
# @rest_method("GET")
# def request_method(url, endpoint, client_id, headers, auth=None, data=None):
#     return requests.request(
#         url=f"{url}{endpoint}{client_id}",
#         headers=headers,
#         auth=auth,
#         json=data,
#     )


# print(request_method("https://smth/",
#                      "/clients",
#                      "",
#                      {"accept": "application/json", "X-API-KEY": "invalid_api_key"}
#                      ).content)

# def post(func):
#     def wrapper(url, endpoint, client_id, headers, crud="POST", auth=None, data=None):
#         return func(url, endpoint, client_id, headers, method=crud, auth=auth, data=data)
#
#     return wrapper
#
#
# def get(func):
#     def wrapper(url, endpoint, client_id, headers, crud="GET", auth=None, data=None):
#         return func(url, endpoint, client_id, headers, method=crud, auth=auth, data=data)
#
#     return wrapper
#
#
# def patch(func):
#     def wrapper(url, endpoint, client_id, headers, crud="PUT", auth=None, data=None):
#         return func(url, endpoint, client_id, headers, method=crud, auth=auth, data=data)
#
#     return wrapper
#
#
# def delete(func):
#     def wrapper(url, endpoint, client_id, headers, crud="DELETE", auth=None, data=None):
#         return func(url, endpoint, client_id, headers, method=crud, auth=auth, data=data)
#
#     return wrapper


# @get
# def request_method(url, endpoint, client_id, headers, crud, auth=None, data=None):
#     return requests.request(
#         method=crud,
#         url=f"{url}{endpoint}{client_id}",
#         headers=headers,
#         auth=auth,
#         json=data,
#     )





#     if headers is None:
#         headers = {"accepts": "application/json", "X-API-KEY": "invalid_api_key"}


# def decorator_function(func):
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#
#     return wrapper
#
#
# @decorator_function
# def display(a, b, c):
#     return "return smth", a, b, c
#
#
# print(display("kurka", "wolna", None))