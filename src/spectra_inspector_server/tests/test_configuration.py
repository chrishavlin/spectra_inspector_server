# mypy: disable-error-code="no-untyped-def"
from spectra_inspector_server._file_tree_handling import PathHandler


def test_PathHandler(tmp_path):

    root_dir = tmp_path / "spectra_root"
    root_dir.mkdir()
    ph = PathHandler(root_dir)

    EDAX_files = ph.get_sample_edax_file_names("C2")
    assert EDAX_files.spc.suffix == ".spc"
