from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from spectra_inspector_server.dependencies import get_database_session, get_settings
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


@app.get("/image_metadata")
async def image_metadata(sample_name: str):

    ph = get_database_session()
    if sample_name in ph.database.available_maps:
        fl = ph.load_edax(sample_name)
        return fl.refined_metadata

    msg = f"{sample_name} is not an available image dataset"
    raise HTTPException(status_code=404, detail=msg)
