import numpy as np
import pytest
from fastapi.testclient import TestClient

from spectra_inspector_server._testing import _on_disc_mock
from spectra_inspector_server.main import app
from spectra_inspector_server.model import MetadataModel, Spectrum1dDict

client = TestClient(app)

_endpoints_keys = [
    ("info", ["app_name", "spectra_inspector_data_root"]),
    ("available-datasets", ["available_files"]),
]


@pytest.mark.parametrize(("endpoint", "response_keys"), _endpoints_keys)
def test_endpoint_responses(endpoint: str, response_keys: list[str] | None) -> None:

    response = client.get(f"/{endpoint}")
    assert response.status_code == 200

    if response_keys:
        jdict = response.json()
        all(ky in jdict for ky in response_keys)


def test_image_metadata() -> None:
    response = client.get(
        "/image-metadata", params={"sample_name": _on_disc_mock.filenames[0]}
    )
    assert response.status_code == 200
    mm = MetadataModel(**response.json())
    assert mm.General.title == "EDS Spectrum Image"


def test_image_spectrum() -> None:

    response = client.get(
        "/image-spectrum", params={"sample_name": _on_disc_mock.filenames[0]}
    )
    assert response.status_code == 200
    spectrum = Spectrum1dDict(**response.json())
    assert np.all(np.isreal(spectrum.energy))
    assert np.all(np.isreal(spectrum.intensity))
