from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel

from spectra_inspector_server.processor.utilities import _get_nested_dict_element


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


@dataclass
class Spectrum1d:
    energy: npt.NDArray
    intensity: npt.NDArray


class GeneralMetadata(BaseModel):
    original_filename: str
    title: str


class Signal(BaseModel):
    signal_type: str


class EDS(BaseModel):
    azimuth_angle: float
    elevation_angle: float
    energy_resolution_MnKa: float
    live_time: float


class Detector(BaseModel):
    EDS: EDS


class Stage(BaseModel):
    tilt_alpha: float


class SEM(BaseModel):
    Detector: Detector
    beam_energy: float
    Stage: Stage


class AcquisitionInstrument(BaseModel):
    SEM: SEM


class Sample(BaseModel):
    elements: list[str]


class MetadataModel(BaseModel):
    General: GeneralMetadata
    Signal: Signal
    Acquisition_instrument: AcquisitionInstrument
    Sample: Sample


class EDAX_raw_ds:
    data: npt.NDArray  # type: ignore[type-arg]
    axes: list[EDAX_axis]
    metadata: dict[str, Any]
    original_metadata: dict[str, Any]
    axes_by_index: dict[int, EDAX_axis]

    def __init__(self, raw_ds: dict[str, Any]):

        axes = [EDAX_axis(**ax_dict) for ax_dict in raw_ds["axes"]]

        valid_data: np.ndarray = raw_ds["data"]  # type: ignore[type-arg]
        self.data = valid_data
        self.axes = axes
        self.metadata = raw_ds["metadata"]
        self.original_metadata = raw_ds["original_metadata"]

        axes_by_index: dict[int, EDAX_axis] = {}
        for ax in axes:
            axes_by_index[ax.index_in_array] = ax
        self.axes_by_index = axes_by_index

    @property
    def refined_metadata(self) -> MetadataModel:
        md = self.metadata
        gm = GeneralMetadata(**md["General"])
        sig = Signal(**md["Signal"])

        eds = _get_nested_dict_element(
            md, ["Acquisition_instrument", "SEM", "Detector", "EDS"]
        )
        eds["azimuth_angle"] = float(eds["azimuth_angle"])
        eds["elevation_angle"] = float(eds["elevation_angle"])
        eds["energy_resolution_MnKa"] = float(eds["energy_resolution_MnKa"])
        eds["live_time"] = float(eds["live_time"])
        eds_inst = EDS(**eds)
        det = Detector(EDS=eds_inst)

        stage_dict = _get_nested_dict_element(
            md, ["Acquisition_instrument", "SEM", "Stage"]
        )
        stage_dict["tilt_alpha"] = float(stage_dict["tilt_alpha"])
        stage = Stage(**stage_dict)

        beam_energy = float(
            _get_nested_dict_element(
                md, ["Acquisition_instrument", "SEM", "beam_energy"]
            )
        )
        sem = SEM(Detector=det, Stage=stage, beam_energy=beam_energy)

        ai = AcquisitionInstrument(SEM=sem)

        samp = Sample(elements=md["Sample"]["elements"])

        return MetadataModel(
            General=gm,
            Signal=sig,
            Acquisition_instrument=ai,
            Sample=samp,
        )
