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

### Testing

To run unit tests with Pytest

```sh
python -m pytest
# or
pytest .
```
