from faker.providers import BaseProvider
from pysam import AlignedSegment

from ..reads.read_generator import QualityModel, ReadGenerator
from ..ref.enums import VariantType


class ReadProvider(BaseProvider):
    """
    Custom Faker provider that generates synthetic reads.

    Example:
        >>> from faker import Faker
        >>> fake = Faker()
        >>> fake.add_provider(ReadProvider)
        >>> read = fake.read()
        >>> print(read.sequence)
        'ACGTACGTAC'
    """

    def read(
        self,
        reference_position: int = 100,
        reference_sequence: str = "ATGCTGTG",
        error_probabilities: dict[VariantType, float] | None = None,
    ) -> AlignedSegment:
        quality_model = QualityModel()
        generator = ReadGenerator(
            quality_model=quality_model, error_probabilities=error_probabilities
        )
        return generator.generate(reference_position, reference_sequence)
