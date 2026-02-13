from spectra_inspector_server._file_tree_handling import PathHandler


def get_sample_axes_info(ph: PathHandler, sample_name: str):
    edax_ds = ph.load_edax(sample_name)
    axes_info = edax_ds.axes.copy()
    del edax_ds
    return axes_info
