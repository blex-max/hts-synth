from collections.abc import Iterable, Iterator

import pysam
from pysam import AlignedSegment

from ..ref.enums import VariantType
from ..ref.generate_variant import VariantGenerator
from ..ref.reference import ReferenceSegment


class QualityModel:
    """
    Placeholder class for generating quality scores for synthetic reads.

    This class provides functionality to generate quality scores for sequences
    of specified lengths. Currently serves as a placeholder implementation.
    """

    def get_quality_scores(self, length: int) -> Iterable[int]:
        """
        Generate quality scores for a sequence of given length.

        Args:
            length (int): The length of the sequence to generate quality scores for.

        Returns:
            Iterable[int]: An iterable of integer quality scores, currently all zeros as placeholder.

        Example:
            >>> model = QualityModel()
            >>> scores = list(model.get_quality_scores(5))
            >>> print(scores)  # [0, 0, 0, 0, 0]
        """
        return [0 for _ in range(length)]


class ReadGenerator:
    """
    Generate synthetic sequencing reads with simulated errors.

    This class creates synthetic reads by applying sequencing errors (insertions,
    deletions, and substitutions) to reference sequences based on configurable
    error probabilities.

    Attributes:
        quality_model (QualityModel): Object that provides quality score generation functionality.
        error_probabilities (dict[VariantType, float]): Dictionary mapping VariantType to error probability rates.

    Example:
        >>> quality_model = QualityModel()
        >>> generator = ReadGenerator(quality_model)
        >>> read = generator.generate(100, "ATCGATCG")
    """

    error_probabilities: dict[VariantType, float] = {
        VariantType.INSERTION: 0.01,
        VariantType.DELETION: 0.01,
        VariantType.SUBSTITUTION: 0.05,
    }

    def __init__(
        self,
        reference_segment: ReferenceSegment | str,
        quality_model: QualityModel,
        error_probabilities: dict[VariantType, float] | None = None,
        paired: bool = True
    ):
        """
        Initialize a ReadGenerator with quality model and error probabilities.

        Args:
            quality_model (QualityModel): Object that provides quality score generation functionality.
            error_probabilities (dict[VariantType, float] | None): Optional dictionary mapping VariantType to error
                probability rates. If None, uses class default values.

        Example:
            >>> quality_model = QualityModel()
            >>> custom_errors = {VariantType.SUBSTITUTION: 0.02}
            >>> generator = ReadGenerator(quality_model, custom_errors)
        """
        self.reference_segment: ReferenceSegment | str = reference_segment

        self.quality_model: QualityModel = quality_model

        if error_probabilities:
            self.error_probabilities = error_probabilities

        self.paired = paired

    def _generate(self) -> AlignedSegment:
        """
        Generate a single synthetic read with simulated sequencing errors.

        Applies mutations based on configured error probabilities to create a
        realistic synthetic read from the reference sequence.

        Args:
            reference_position (int): The starting position within the reference genome
                where this read originates.
            reference_sequence (str): The reference DNA sequence to use as the basis
                for read generation.

        Returns:
            AlignedSegment: An AlignedSegment object representing the synthetic read with:
                - Mutated sequence based on error probabilities
                - Quality scores from the quality model
                - Basic alignment properties set

        Note:
            The returned read currently has placeholder values for some properties
            like read name and mapping quality. Future versions will generate
            more realistic values.

        Example:
            >>> generator = ReadGenerator(QualityModel())
            >>> read = generator.generate(100, "ATCGATCG")
            >>> print(read.query_sequence)  # Potentially mutated sequence
        """

        # Get segment sequence if held in class
        if type(self.reference_segment) == ReferenceSegment:
            input_sequence = self.reference_segment.sequence
        elif type(self.reference_segment) == str:
            input_sequence = self.reference_segment
        else:
            raise ValueError("Generator reference segment must be either a 'ReferenceSegment' or a str")

        # Generate numbers of events based on error probabilities dict
        # [num_insertions, num_deletions, num_substitutions]
        events = [
            round(rate * len(input_sequence)) for rate in self.error_probabilities.values()
        ]

        variant_generator = VariantGenerator(input_sequence, events)

        read = AlignedSegment()

        read.query_sequence = "".join(
            variant.alt for variant in variant_generator.generate_random_variant_sequence()
        )
        print(self.quality_model.get_quality_scores(len(read.query_sequence)))
        read.query_qualities_str = pysam.qualities_to_qualitystring(
            qualities=self.quality_model.get_quality_scores(len(read.query_sequence))  # pyright: ignore[reportArgumentType]
        )

        # TODO actually generate read properties - meaningful name and correct flag
        # Should this function return a pair of reads for paired end sequencing?
        # Should this be a seperate function?

        read.query_name = "synthetic_read/1"
        read.reference_id = 0

        if type(self.reference_segment) == ReferenceSegment:
            read.reference_start = self.reference_segment.start
            read.next_reference_start = self.reference_segment.start + len(read.query_sequence)

        read.is_paired = self.paired
        read.mapping_quality = 20

        return read

    def emit_reads(self, amount: int = 1) -> Iterator[AlignedSegment]:
        """
        Generate multiple synthetic reads from the same reference sequence.

        Creates a specified number of independent synthetic reads, each with
        potentially different mutations applied based on the error probabilities.

        Args:
            reference_position (int): The starting position within the reference genome
                where these reads originate.
            reference_sequence (str): The reference DNA sequence to use as the basis
                for read generation.
            amount (int): The number of reads to generate. Defaults to 10.

        Yields:
            AlignedSegment: Individual synthetic reads, each potentially containing
                different mutations from the same reference sequence.

        Example:
            >>> generator = ReadGenerator(QualityModel())
            >>> reads = list(generator.generate_multiple(100, "ATCGATCG", 5))
            >>> len(reads)  # 5
        """
        for _ in range(amount):
            yield self._generate()
