[![python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=FFD43B)](https://docs.python.org/3.12/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-D7FF64?style=for-the-badge&logo=ruff)](https://docs.astral.sh/ruff/)
[![license](https://img.shields.io/badge/License-MIT-a51931?style=for-the-badge)](LICENSE.txt)

# hts-synth

Biodev Hackathon 2025 - constrained generation of HTS data for testing and exploration.

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

### Testing

To run unit tests with Pytest

```sh
python -m pytest
# or
pytest .
```
