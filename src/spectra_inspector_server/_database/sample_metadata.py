import json
from pathlib import Path

import pandas as pd

from spectra_inspector_server.model import sampleMetadata, sampleMetadataCSVrecord

# expected CSV format
#
# sample_id, lat, lon
# C-12, -50.953878, -72.983542


class SampleMetadataMapper:
    sample_metadata_fullpath: Path
    exists: bool
    _df: pd.DataFrame | None = None
    expected_cols = ("sample_id", "lat", "lon")

    def __init__(self, sample_metadata_fullpath: Path):
        self.sample_metadata_fullpath = sample_metadata_fullpath
        self.exists = sample_metadata_fullpath.is_file()

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None and self.exists:
            self._df = pd.read_csv(self.sample_metadata_fullpath)
        if self._df is None:
            msg = f"Could not find CSV Metadata file: {self.sample_metadata_fullpath}"
            raise FileNotFoundError(msg)
        return self._df

    def get_sample(self, sample_id: str) -> sampleMetadataCSVrecord | None:
        dfi = self.df[self.df.sample_id == sample_id]
        if len(dfi) == 1:
            return sampleMetadataCSVrecord(**dfi.iloc[0].to_dict())
        return None

    def get_all(self) -> sampleMetadata:
        recs = json.loads(self.df.to_json(orient="records"))
        records = [sampleMetadataCSVrecord(**rec) for rec in recs]
        return sampleMetadata(records=records)

    @property
    def columns(self) -> list[str]:
        cols = self.df.columns.to_list()
        if set(cols) != set(self.expected_cols):
            msg = "CSV columns do not match expected format"
            raise RuntimeError(msg)
        return cols
