import click

from hts_synth.providers.read_provider import generate_read


@click.command()
@click.option("--length", default=10, help="Number of base pairs.")
def cli(length: int):
    """Synthesise a HTS read."""
    # TODO: Replace with actual read generation method once implemented
    read = generate_read(length=length)
    click.echo(read.sequence)
    click.echo(read.quality_string)
