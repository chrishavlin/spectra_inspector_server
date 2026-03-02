from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from spectra_inspector_server.dependencies import get_database_session, get_settings
from spectra_inspector_server.processor.operations import OperationEDAXStateHandler
from spectra_inspector_server.settings import Settings

app = FastAPI()


@app.get("/info")
async def info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "spectra_inspector_data_root": settings.spectra_inspector_data_root,
    }


@app.get("/available-datasets")
async def avaialbe_datasets() -> dict[str, list[str]]:

    ph = get_database_session()
    filekeys = [str(nm) for nm in ph.database.available_maps]
    return {"available_files": filekeys}


@app.get("/image-metadata")
async def image_metadata(sample_name: str):

    ph = get_database_session()
    if sample_name not in ph.database.available_maps:
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph)
    return ops.get_refined_metadata(sample_name)


@app.get("/image-spectrum")
async def image_spectrum(
    sample_name: str,
):

    ph = get_database_session()
    if sample_name not in ph.database.available_maps:
        msg = f"{sample_name} is not a valid sample"
        raise HTTPException(404, detail=msg)

    ops = OperationEDAXStateHandler(ph)
    result = ops.get_spectrum(
        sample_name,
        # TODO: optional args
    )
    return result.todict()
