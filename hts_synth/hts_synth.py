import click

from .reads.read_generator import QualityModel, ReadGenerator
from .ref.enums import VariantType


@click.command()
@click.option(
    "--reference_position",
    default=100,
    help="The starting position within the reference genome where this read originates.",
)
@click.option(
    "--reference_sequence",
    default="ATGCTGTG",
    help="The reference DNA sequence to use as the basis for read generation.",
)
@click.option(
    "--error_probabilities",
    default=None,
    help="""JSON string mapping variant type numbers to error probabilities, 
    e.g., \'{"0": 0.01, "1": 0.01, "2": 0.02}\' 
    (0=INSERTION, 1=DELETION, 2=SUBSTITUTION)""",
)
def cli(
    reference_position: int,
    reference_sequence: str,
    error_probabilities: dict[VariantType, float] | None = None,
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
    generator = ReadGenerator(quality_model=quality_model, error_probabilities=error_probabilities)

    read = generator.generate(reference_position, reference_sequence)
    click.echo(read.query_sequence)
    click.echo(read.query_qualities_str)
