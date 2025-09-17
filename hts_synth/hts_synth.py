import click

from .reads.read_generator import QualityModel, ReadGenerator
from .ref.enums import VariantType


@click.command()
@click.argument(
    "reference_sequence",
    help="The reference DNA sequence to use as the basis for read generation.",
)
@click.option(
    "--reference_position",
    default=0,
    help="The starting position within the reference genome where this read originates.",
    type=int,
)
@click.option(
    "--insertion-probability",
    default=0.01,
    help="The probability that the read generated will include an insertion",
    type=float,
)
@click.option(
    "--deletion-probability",
    default=0.01,
    help="The probability that the read generated will include an deletion",
    type=float,
)
@click.option(
    "--substitution-probability",
    default=0.02,
    help="The probability that the read generated will include a substitution",
    type=float,
)
def cli(
    reference_position: int,
    reference_sequence: str,
    insertion_probability: float,
    deletion_probability: float,
    substitution_probability: float,
):
    """
    Generate synthetic HTS read data from a reference sequence.

    Creates a synthetic high-throughput sequencing read based on the provided
    reference sequence and position. The function applies configurable error
    probabilities for various variant types (insertions, deletions, substitutions)
    to simulate realistic sequencing errors.

    Args:
        reference_position: The starting genomic position for the read (default: 100)
        reference_sequence: The DNA reference sequence string (default: "ATGCTGTG")
        error_probabilities: Optional mapping of variant types to error rates

    Returns:
        Outputs the generated read sequence and quality scores to stdout
    """
    quality_model = QualityModel()
    error_probabilities = {
        VariantType.INSERTION: insertion_probability,
        VariantType.DELETION: deletion_probability,
        VariantType.SUBSTITUTION: substitution_probability,
    }
    generator = ReadGenerator(
        quality_model=quality_model, error_probabilities=error_probabilities
    )

    read = generator.generate(reference_position, reference_sequence)
    click.echo(read.query_sequence)
    click.echo(read.query_qualities_str)
