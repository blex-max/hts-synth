import pytest
from faker import Faker

from hts_synth.providers.read_provider import ReadProvider


@pytest.fixture(scope="session")
def faker():
    faker = Faker()
    faker.add_provider(ReadProvider)
    yield faker
