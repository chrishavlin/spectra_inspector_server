from spectra_inspector_server._testing import _on_disc_mock
from spectra_inspector_server.processor.operations import (
    get_sample_axes_info,
)


def test_get_sample_axes_info(edax_path_handler):
    fake_filename = _on_disc_mock.filenames[0]
    axis_info = get_sample_axes_info(edax_path_handler, fake_filename)
    assert len(axis_info) == 3
