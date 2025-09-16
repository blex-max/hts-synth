from faker import Faker
from pysam import AlignedSegment


class TestRead:
    def test_read(self, faker: Faker):
        read: AlignedSegment = faker.read(10)
        sequence = read.query_sequence
        assert sequence is not None
        assert len(sequence) == 10

        read2: AlignedSegment = faker.read(5)
        sequence2 = read2.query_sequence
        assert sequence2 is not None
        assert len(sequence2) == 5
