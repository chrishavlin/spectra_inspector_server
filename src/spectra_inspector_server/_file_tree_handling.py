import os
from pathlib import Path

from spectra_inspector_server._logging import spectraLogger
from spectra_inspector_server.model import EDAX_file_set, EDAX_raw_ds
from spectra_inspector_server.processor.file_loaders import load_edax_spd

_ENV_DATA_ROOT = "SPECTRAINSPECTORDATAROOT"


class PathHandler:
    data_root: Path
    edax_dir_name: str = "Proprietary EDAX Files"

    def __init__(self, data_root: str | Path | None = None):

        valid_data_path: Path | None = None
        if data_root is None:
            if envval := os.environ.get(_ENV_DATA_ROOT):
                valid_data_path = Path(envval)
        else:
            valid_data_path = Path(data_root)

        if valid_data_path is None:
            msg = f"Could not identify data root directory, provide to PathHandler or set the environment variable {_ENV_DATA_ROOT}"
            raise ValueError(msg)

        self.data_root = Path(valid_data_path)

        if not Path.exists(self.data_root):
            msg = f"data_root path does not exist: {self.data_root}"
            raise FileNotFoundError(msg)

        spectraLogger.info(f"Initialized PathHandler with data_root {self.data_root}")

    def get_sample_dir(self, sample_name: str) -> Path:
        return self.data_root / sample_name / self.edax_dir_name

    def get_sample_edax_file_names(self, sample_name: str) -> EDAX_file_set:

        sdir = self.get_sample_dir(sample_name)

        fullfiles = {}
        for ext in ["spd", "spc", "ipr", "bmp", "xml"]:
            fullfiles[ext] = sdir / f"{sample_name}.{ext}"

        return EDAX_file_set(**fullfiles)

    def load_edax(self, sample_name: str) -> EDAX_raw_ds:
        files = self.get_sample_edax_file_names(sample_name)
        return load_edax_spd(files)
