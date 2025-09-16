import random
import string

from faker.providers import BaseProvider
from hts_synth.wrappers.sam_wrapper import create_synthetic_read_pair
from pysam import AlignedSegment


def generate_read(length=10):
    # TODO: Replace with actual read generation method once implemented
    seq = "".join(random.choices("ACGT", k=length))
    qual = "".join(random.choices(string.ascii_letters, k=length))

    return create_synthetic_read_pair(seq, qual)


class ReadProvider(BaseProvider):
    """
    Example scaffolding for a custom Faker provider that generates synthetic reads.

    This class demonstrates the basic structure needed to create a custom provider
    for the Faker library. It extends BaseProvider and implements a single method
    to generate Read objects.

    Example:
        >>> from faker import Faker
        >>> fake = Faker()
        >>> fake.add_provider(ReadProvider)
        >>> read = fake.read()
        >>> print(read.sequence)
        'ACGTACGTAC'
    """

    def read(self, length: int = 10) -> AlignedSegment:
        return generate_read(length=length)
