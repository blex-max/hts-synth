from faker import Faker
from pysam import AlignedSegment


class TestReadProvider:
    def test_read(self, faker: Faker):
        read: AlignedSegment = faker.read()
        sequence = read.query_sequence
        assert sequence is not None
