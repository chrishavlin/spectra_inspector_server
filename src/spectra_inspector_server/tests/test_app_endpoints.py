import pytest
from fastapi.testclient import TestClient

from spectra_inspector_server.main import app

client = TestClient(app)

_endpoints_keys = [
    ("info", ["app_name", "spectra_inspector_data_root"]),
    ("available-datasets", ["available_files"]),
]


@pytest.mark.parametrize(("endpoint", "response_keys"), _endpoints_keys)
def test_endpoint_responses(endpoint: str, response_keys: list[str] | None):
    response = client.get(f"/{endpoint}")
    assert response.status_code == 200

    if response_keys:
        jdict = response.json()
        all(ky in jdict for ky in response_keys)
