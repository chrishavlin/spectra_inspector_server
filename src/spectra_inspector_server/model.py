from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel


class EDAX_file_set(BaseModel):
    spd: Path
    spc: Path
    ipr: Path
    bmp: Path
    xml: Path


@dataclass
class EDAX_axis:
    size: int
    index_in_array: int
    name: str
    scale: np.float32
    offset: int
    units: str
    navigate: bool


class EDAX_raw_ds:
    data: npt.NDArray  # type: ignore[type-arg]
    axes: list[EDAX_axis]
    metadata: dict[str, Any]
    original_metadata: dict[str, Any]

    def __init__(self, raw_ds: dict[str, Any]):

        axes = [EDAX_axis(**ax_dict) for ax_dict in raw_ds["axes"]]

        valid_data: np.ndarray = raw_ds["data"]  # type: ignore[type-arg]
        self.data = valid_data
        self.axes = axes
        self.metadata = raw_ds["metadata"]
        self.original_metadata = raw_ds["original_metadata"]
