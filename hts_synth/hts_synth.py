import os
import sys
import uuid
from typing import Literal

import click

from .reads.read_generator import QualityModel, ReadGenerator
from .ref.enums import VariantType
from .ref.reference import Reference

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c",
    "--reference-chrom",
    type=str,
    help="The chromosome within the reference genome where this read originates.",
)
@click.option(
    "-s",
    "--reference-start",
    default=0,
    show_default=True,
    type=int,
    help="The starting position within the reference genome where this read originates.",
)
@click.option(
    "-e",
    "--reference-end",
    type=int,
    help="The end position within the reference genome where this read originates.",
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
@click.option(
    "-f",
    "--out-format",
    show_default=True,
    default="fq",
    type=click.Choice(["fq", "seq", "qual"]),
    help="format of the output",
)
@click.argument(
    "reference-sequence",
    metavar="REF",
)
@click.argument("n-reads", metavar="NREADS", default=1, type=int)
def cli(
    reference_chrom: str | None,
    reference_start: int,
    reference_end: int,
    reference_sequence: str,
    insertion_probability: float,
    deletion_probability: float,
    substitution_probability: float,
    n_reads: int = 1,
    out_format: Literal["fq", "seq", "qual"] = "fq",  # should probably use an enum
):
    """
    Generate synthetic HTS read data from a reference sequence.

    Creates a synthetic high-throughput sequencing read based on the provided
    reference sequence and position. The function applies configurable error
    probabilities for various variant types (insertions, deletions, substitutions)
    to simulate realistic sequencing errors.

    Returns:\n
        Outputs the generated read sequence and quality scores to stdout
    """  # noqa: D301
    quality_model = QualityModel()
    error_probabilities = {
        VariantType.INSERTION: insertion_probability,
        VariantType.DELETION: deletion_probability,
        VariantType.SUBSTITUTION: substitution_probability,
    }

    if os.path.exists(reference_sequence):
        reference = Reference(reference_sequence)

        if not reference_chrom or not reference_end:
            click.echo("", err=True)
            sys.exit(1)

        reference_segment = reference.get_sequence(reference_chrom, reference_start, reference_end)

        generator = ReadGenerator(reference_segment, quality_model, error_probabilities)
    else:
        generator = ReadGenerator(reference_sequence, quality_model, error_probabilities)

    for read in generator.emit_reads(n_reads):
        match out_format:
            case "fq":
                click.echo(f"@read-{str(uuid.uuid4())[:16]}")
                click.echo(read.query_sequence)
                click.echo("+")
                click.echo(read.query_qualities_str)
            case "seq":
                click.echo(read.query_sequence)
            case "qual":
                click.echo(read.query_qualities_str)
