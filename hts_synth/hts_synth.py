from typing import Literal
import click
import uuid

from .reads.read_generator import QualityModel, ReadGenerator
from .ref.enums import VariantType


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-p",
    "--reference-position",
    default=0,
    show_default=True,
    type=int,
    help="The starting position within the reference genome where this read originates.",
)
@click.option(
    "--error-probabilities",
    default=None,  # TODO: surface the default
    help="""JSON string mapping variant type numbers to error probabilities, 
    e.g., \'{"0": 0.01, "1": 0.01, "2": 0.02}\' 
    (0=INSERTION, 1=DELETION, 2=SUBSTITUTION)""",
)
@click.option(
    "-f",
    "--out-format",
    show_default=True,
    default="fq",
    type=click.Choice(["fq", "seq", "qual"]),
    help="format of the output"
)
@click.argument(
    "n-reads",
    metavar='NREADS',
    default=1,
    type=int,
)
@click.argument(
    "reference-sequence",
    metavar="REF"
)
def cli(
    reference_position: int,
    reference_sequence: str,
    error_probabilities: dict[VariantType, float] | None = None,
    n_reads: int = 1,
    out_format: Literal["fq", "seq", "qual"] = "fq"  # should probably use an enum
):
    """
    Generate synthetic HTS read data from a reference sequence.

    Creates a synthetic high-throughput sequencing read based on the provided
    reference sequence and position. The function applies configurable error
    probabilities for various variant types (insertions, deletions, substitutions)
    to simulate realistic sequencing errors.

    Args:
        reference_position: The starting genomic position for the read (default: 0)
        reference_sequence: The DNA reference sequence string
        error_probabilities: Optional mapping of variant types to error rates

    Returns:
        Outputs the generated read sequence and quality scores to stdout
    """
    quality_model = QualityModel()
    generator = ReadGenerator(quality_model=quality_model, error_probabilities=error_probabilities)

    for _ in range(n_reads):
        read = generator.generate(reference_position, reference_sequence)
        match out_format:
            case "fq":
                click.echo(f"@read-{str(uuid.uuid4())[:16]}")
                click.echo(read.query_sequence)
                click.echo('+')
                click.echo(read.query_qualities_str)
            case "seq":
                click.echo(read.query_sequence)
            case "qual":
                click.echo(read.query_qualities_str)
