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
