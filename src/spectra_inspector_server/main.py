from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException

from spectra_inspector_server._file_tree_handling import EDAXPathHandler
from spectra_inspector_server._logging import spectraLogger
from spectra_inspector_server._testing import pytest_running
from spectra_inspector_server.dependencies import get_database_session, get_settings
from spectra_inspector_server.model import (
    AvailableDatasets,
    CombinedMetadata,
    Info,
    MetadataModel,
    Spectrum1dDict,
    raveledImage,
)
from spectra_inspector_server.processor.operations import OperationEDAXStateHandler
from spectra_inspector_server.settings import Settings

app = FastAPI()


def _valid_sample_name(sample_name: str, ph: EDAXPathHandler) -> bool:
    if sample_name in ph.database.available_maps:
        return True

    if pytest_running():
        from spectra_inspector_server._testing import _on_disc_mock  # noqa: PLC0415

        return sample_name in _on_disc_mock.filenames

    return False


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]) -> Info:
    return Info(
        app_name=settings.app_name,
        spectra_inspector_data_root=settings.spectra_inspector_data_root,
    )


@app.get("/available-datasets")
async def avaialbe_datasets() -> AvailableDatasets:

    ph = get_database_session()
    filekeys = [str(nm) for nm in ph.database.available_maps]
    return AvailableDatasets(available_files=filekeys)


@app.get("/image-metadata")
async def image_metadata(sample_name: str) -> MetadataModel:

    ph = get_database_session()
    if not _valid_sample_name(sample_name, ph):
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph, allow_mock_files=pytest_running())
    return ops.get_refined_metadata(sample_name)


@app.get("/image-metadata-combined")
async def image_metadata_combined(sample_name: str) -> CombinedMetadata:

    ph = get_database_session()
    if not _valid_sample_name(sample_name, ph):
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph, allow_mock_files=pytest_running())
    return ops.get_combined_metadata(sample_name)


@app.get("/image-spectrum")
async def image_spectrum(
    sample_name: str,
) -> Spectrum1dDict:

    ph = get_database_session()
    if not _valid_sample_name(sample_name, ph):
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph, allow_mock_files=pytest_running())
    result = ops.get_spectrum(
        sample_name,
        # TODO: optional args
    )
    return result.todict()


@app.get("/image-data")
async def image_data(
    sample_name: str,
    channel_index: int,
    index0_0: int | None | Literal["none"] = None,
    index0_1: int | None | Literal["none"] = None,
    index1_0: int | None | Literal["none"] = None,
    index1_1: int | None | Literal["none"] = None,
) -> raveledImage:
    ph = get_database_session()
    if not _valid_sample_name(sample_name, ph):
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph, allow_mock_files=pytest_running())

    index0_range = (index0_0, index0_1)
    if index0_0 == "none":
        index0_0 = None
    if index0_1 == "none":
        index0_1 = None

    if index1_0 == "none":
        index1_0 = None
    if index1_1 == "none":
        index1_1 = None

    result = ops.get_image(
        sample_name, channel_index, index0_range=index0_range, index1_range=index1_range
    )
    shp = result.shape
    im = result.ravel().tolist()

    return raveledImage(image=im, shape=shp)


@app.get("/image-data-summed")
async def image_data_summed(
    sample_name: str,
    channel_range: tuple[int, int],
    index0_range: tuple[int, int] | Literal["none"] | None = None,
    index1_range: tuple[int, int] | Literal["none"] | None = None,
) -> raveledImage:
    ph = get_database_session()
    if not _valid_sample_name(sample_name, ph):
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph, allow_mock_files=pytest_running())

    if index0_range == "none":
        index0_range = None
    if index1_range == "none":
        index1_range = None

    msg = f"fetching summed channel intensity for {sample_name} with {channel_range=}, {index0_range=}, {index1_range=}"
    spectraLogger.info(msg)

    result = ops.get_multi_channel_intensity_image(
        sample_name, channel_range, index0_range=index0_range, index1_range=index1_range
    )

    shp = result.shape
    im = result.ravel().tolist()

    return raveledImage(image=im, shape=shp)
