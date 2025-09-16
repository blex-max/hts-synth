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

$ hts-synth --length=20                                                                         10:41:52
TTCATCTAAAATATATGAAC
klPsyRcqfervojkGHICH
```

## Development

### Requirements

- Python 3.12+
- Pyenv

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
