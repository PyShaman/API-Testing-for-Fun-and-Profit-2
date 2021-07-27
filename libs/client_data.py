"""
client_data.py - zamiast tworzenia słownika, proponuję stworzyć klasę używając @dataclass,
później można użyc na tym metody asdict() i otrzymasz ten sam słownik, który
zwracasz (asdict używj podczas wysyłki klasy User)
"""

from dataclasses import dataclass, asdict
from faker import Faker


@dataclass
class ClientData:
    firstName: str
    lastName: str
    phone: str


def return_client_data():
    faker = Faker("pl_PL")
    cd = ClientData(faker.first_name(), faker.last_name(), faker.phone_number())
    return asdict(cd)
