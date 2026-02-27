from pathlib import Path
from typing import TYPE_CHECKING

from spectra_inspector_server._logging import spectraLogger
from spectra_inspector_server.model import EDAX_file_set

if TYPE_CHECKING:
    from spectra_inspector_server._file_tree_handling import EDAXPathHandler


class OnDiskDatabase:
    available_maps: dict[str:EDAX_file_set]

    def __init__(self, ph: "EDAXPathHandler", init_db: bool = True):
        self.available_maps = {}
        if init_db:
            self.inspect(ph)

    def inspect(self, ph):
        spectraLogger.info(f"Inspecting {ph.data_root}")
        _recursive_inspection(ph.data_root, self)

    def add_fileset(self, basename: str, files: dict[str, Path]):
        if basename in self.available_maps:
            msg = f"Duplicate map name! {basename} exists already."
            raise KeyError(msg)

        new_set = EDAX_file_set(**files)
        spectraLogger.debug(f"adding {basename} to available_maps")
        self.available_maps[basename] = new_set


_expected_exts = [".spd", ".spc", ".ipr", ".bmp", ".xml"]


def _get_expected_files(spd_file: Path) -> dict[str, Path]:
    basename = spd_file.stem

    file_set_args = {}
    for ext in _expected_exts:
        newfi = basename + ext
        file_set_args[ext.replace(".", "")] = spd_file.parent / newfi

    return file_set_args


def _has_all_files(spd_file: Path):
    for expected_file in _get_expected_files(spd_file).values():
        if not expected_file.is_file():
            return False
    return True


def _recursive_inspection(dirname: Path, db: OnDiskDatabase):
    if dirname.is_dir():
        for fh in dirname.iterdir():
            if fh.is_dir():
                _recursive_inspection(fh, db)
            if fh.is_file() and fh.suffix == ".spd" and _has_all_files(fh):
                # we have a sample!
                db.add_fileset(fh.stem, _get_expected_files(fh))
