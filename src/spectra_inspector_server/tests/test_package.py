from __future__ import annotations

import importlib.metadata

import spectra_inspector_server as m


def test_version():
    assert importlib.metadata.version("spectra_inspector_server") == m.__version__
