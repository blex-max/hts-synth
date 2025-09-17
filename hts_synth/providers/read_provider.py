from faker.providers import BaseProvider
from pysam import AlignedSegment

from ..reads.read_generator import QualityModel, ReadGenerator
from ..ref.enums import VariantType
from ..ref.reference import ReferenceSegment


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
        reference_sequence: ReferenceSegment | str = "ATGCTGTG",
        error_probabilities: dict[VariantType, float] | None = None,
    ) -> AlignedSegment:
        quality_model = QualityModel()
        generator = ReadGenerator(
            reference_segment=reference_sequence,
            quality_model=quality_model,
            error_probabilities=error_probabilities,
        )
        return next(generator.emit_reads(1))
