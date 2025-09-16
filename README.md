[![python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=FFD43B)](https://docs.python.org/3.12/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?style=for-the-badge&logo=ruff)](https://docs.astral.sh/ruff/)
[![license](https://img.shields.io/badge/License-MIT-a51931?style=for-the-badge)](LICENSE.txt)

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
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
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

### Documentation

To generate the documentation, using Sphinx. Run the following commands:

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
