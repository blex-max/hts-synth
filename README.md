[![python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=FFD43B)](https://docs.python.org/3.12/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?style=for-the-badge&logo=ruff)](https://docs.astral.sh/ruff/)
[![license](https://img.shields.io/badge/License-MIT-a51931?style=for-the-badge)](LICENSE.txt)
[![Documentation](https://img.shields.io/badge/Documentation-Online-blue?style=for-the-badge&logo=readthedocs)](https://blex-max.github.io/hts-synth/)

# hts-synth

Biodev Hackathon 2025 - constrained generation of HTS data for testing and exploration.

## Installation

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

## Usage

The synthesising tool can be used both as a Faker provider for unit tests and as a command-line data generator.

### Command line usage

```sh
$ hts-synth --help

$ hts-synth --length=20
TTCATCTAAAATATATGAAC
klPsyRcqfervojkGHICH
```

## Examples

There are usage examples in ./examples. To successfully run the Jyputer notebook, install development the requirements and acquire a FASTQ file for testing. The one that was tested against contains 25 000 reads, each 100 bps long. See [TESTX_H7YRLADXX_S1_L001_R1_001.fastq](https://github.com/hartwigmedical/testdata/tree/master/100k_reads_hiseq/TESTX).

## Development

### Requirements

- Python 3.12+
- Pyenv (optional)
- [Pysam](https://github.com/pysam-developers/pysam)

### Setup

From the repo's base directory

```sh
pyenv install 3.12
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Contributing

The followng checks are automatically run by pre-commit.
If this is the first time you're commiting to this repo, ensure your pre-commit is configured.

Note: you will need to have an SSH public keyadded to your GitHub profile.

```bash
source ./.venv/bin/activate
pre-commit
```

### Linting and Typing

Ruff is used for linting

```sh
python -m ruff format
python -m ruff check --fix
```

Basedpyright for typing

```sh
python -m basedpyright
```

### [Documentation](https://blex-max.github.io/hts-synth/)
Documentation is generated using Sphinx on every commit to the main branch.

#### Local Generation
To generate the documentation locally, using Sphinx. Run the following commands:

```bash
cd docs
make html
```

Then open the generated file documentation/build/html/index.html in your browser to view the documentation.

### Testing

To run unit tests with Pytest

```sh
python -m pytest
# or
pytest .
```

### Authors

- Alex Byrne - Wellcome Sanger Institue (ab63 (at) sanger.ac.uk - Lead Developer/Contact)
- Helen Schuilenburg - Wellcome Sanger Institue (hs21 (at) sanger.ac.uk)
- Hitham Hassan - Wellcome Sanger Institue (hh12 (at) sanger.ac.uk)
- Luca Barbon - Wellcome Sanger Institue (lb29 (at) sanger.ac.uk)
- Rose Neis - EMBL-EBI (rneis (at) ebi.ac.uk)
- Stephen N. Hulme - Wellcome Sanger Institue (stephen.hulme (at) sanger.ac.uk)
- Tom Drever - Wellcome Sanger Institue (td14 (at) sanger.ac.uk)
- Willem S. van Heerden - Wellcome Sanger Institue (wh5 (at) sanger.ac.uk)
