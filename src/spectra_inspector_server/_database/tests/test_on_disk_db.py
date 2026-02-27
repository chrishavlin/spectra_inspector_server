from pathlib import Path
from typing import TYPE_CHECKING

from spectra_inspector_server._database.on_disk_db import _get_expected_files
from spectra_inspector_server._file_tree_handling import EDAXPathHandler

if TYPE_CHECKING:
    from spectra_inspector_server.model import EDAX_file_set


def test_on_disk_db_init(tmp_path):

    # build a test db on disk: this could be a useful fixture
    db_root = tmp_path / "top_db"
    assert isinstance(db_root, Path)
    db_root.mkdir()

    annoying_directory = "annoying second level with spaces"

    sample_names = ["C-1", "C 2", "C 45 map 1", "whatever you want"]
    for sample in sample_names:
        sample_dir = db_root / sample
        sample_dir.mkdir()

        sub_dir = sample_dir / annoying_directory
        sub_dir.mkdir()

        spd_base = sample + ".spd"
        spd_file = sub_dir / spd_base

        sample_files: dict[str, Path] = _get_expected_files(spd_file)
        for sample_file in sample_files.values():
            # write the .spd, .ipr, etc.
            with open(str(sample_file), "w") as fh:
                fh.write(f"writing to {sample_file}")

    # add one more in an existing directory
    new_samp = "lets make another sample"
    sample_names.append(new_samp)
    spd_file = db_root / "C-1" / annoying_directory / (new_samp + ".spd")
    sample_files: dict[str, Path] = _get_expected_files(spd_file)
    for sample_file in sample_files.values():
        with open(str(sample_file), "w") as fh:
            fh.write(f"writing to {sample_file}")

    ph = EDAXPathHandler(data_root=db_root, init_db=True)

    maps: dict[str, EDAX_file_set] = ph.database.available_maps
    assert set(maps.keys()) == set(sample_names)

    for sample in maps.values():
        assert sample.bmp.exists()
        assert sample.spd.exists()
        assert sample.spc.exists()
        assert sample.ipr.exists()
        assert sample.xml.exists()
