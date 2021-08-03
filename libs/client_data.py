from dataclasses import dataclass, asdict, field
from faker import Faker


@dataclass
class ClientData:
    firstName: str = field(default=Faker("pl_PL").first_name())
    lastName: str = field(default=Faker("pl_PL").last_name())
    phone: str = field(default=Faker("pl_PL").phone_number())

    def return_client_data(self):
        return asdict(self)
