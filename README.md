# spectra_inspector_server

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![GitHub Discussion][github-discussions-badge]][github-discussions-link]

[![Coverage][coverage-badge]][coverage-link]

## developer notes

### local setup

Environment setup, install

```
uv venv
source .venv/bin/activate
uv pip install -e .
```

```
fastapi run src/spectra_inspector_server/main.py
```

Visit http://0.0.0.0:8000/docs to check the API, test calls via browser.

### Configuration

Copy `default.env` to `.env` and modify as needed. Some defaults may be set by
environment variables as well, with preference given to the values in `.env`.

#### `SPECTRA_INSPECTOR_DATA_ROOT`

When using a local filesystem repository, the top-level directory of the
directory to search recursively for EDAX file sets. When not set in `.env`, the
default value will be detected from a standard environment variable of the same
name and if not found, will default to `./`.

### manual type checking

```
uv sync
mypy --follow-untyped-imports .
```

<!-- SPHINX-START -->

<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/chrishavlin/spectra_inspector_server/workflows/CI/badge.svg
[actions-link]:             https://github.com/chrishavlin/spectra_inspector_server/actions
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/spectra_inspector_server
[conda-link]:               https://github.com/conda-forge/spectra_inspector_server-feedstock
[github-discussions-badge]: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
[github-discussions-link]:  https://github.com/chrishavlin/spectra_inspector_server/discussions
[pypi-link]:                https://pypi.org/project/spectra_inspector_server/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/spectra_inspector_server
[pypi-version]:             https://img.shields.io/pypi/v/spectra_inspector_server
[rtd-badge]:                https://readthedocs.org/projects/spectra_inspector_server/badge/?version=latest
[rtd-link]:                 https://spectra_inspector_server.readthedocs.io/en/latest/?badge=latest
[coverage-badge]:           https://codecov.io/github/chrishavlin/spectra_inspector_server/branch/main/graph/badge.svg
[coverage-link]:            https://codecov.io/github/chrishavlin/spectra_inspector_server

<!-- prettier-ignore-end -->
