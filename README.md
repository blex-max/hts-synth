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
