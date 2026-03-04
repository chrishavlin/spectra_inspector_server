from functools import lru_cache

from spectra_inspector_server._file_tree_handling import EDAXPathHandler
from spectra_inspector_server.settings import Settings


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_database_session():
    S = get_settings()
    return EDAXPathHandler(data_root=S.spectra_inspector_data_root, init_db=True)
