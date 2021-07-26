import backoff
import requests

from http_constants.headers import HttpHeaders
from requests.auth import HTTPBasicAuth


"""
ten sam plik - pozostań przy oryginalnych get/post itp. Tkod tych metod się mocno powiela i można tutaj wykorzystać 
metodę requests.request('GET') zamiast requests.get i stworzyć sobie dodatkową nadrzętną metodę (za dużo pisania żeby 
podać przykład i jest szansa, że wymyśłisz, jak nie pytaj)
"""


class CrudMethods:

    def __init__(self):
        pass

    @staticmethod
    @backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_time=60)
    def request_method(method, url, endpoint, client_id, data, headers, auth):
        return requests.request(method=method,
                                url=f"{url}{endpoint}{client_id}",
                                json=data,
                                headers=headers,
                                auth=auth)


