import numpy.typing as npt

from spectra_inspector_server._file_tree_handling import EDAXPathHandler
from spectra_inspector_server.model import EDAX_axis


def get_sample_axes_info(ph: EDAXPathHandler, sample_name: str) -> list[EDAX_axis]:
    edax_ds = ph.load_edax(sample_name)
    axes_info = edax_ds.axes.copy()
    del edax_ds
    return axes_info


def get_single_channel_image(
    ph: EDAXPathHandler,
    sample_name: str,
    channel_index: int,
    index0_range: tuple[int, int] | None = None,
    index1_range: tuple[int, int] | None = None,
) -> npt.NDArray:

    edax_ds = ph.load_edax(sample_name)

    input_index_ranges = [index0_range, index1_range]
    valid_index_ranges: list[tuple[int, int]] = []

    for index_id, index_range in enumerate(input_index_ranges):
        valid_range: tuple[int, int]
        if index_range is None:
            valid_range = (0, edax_ds.axes_by_index[index_id].size)
        else:
            valid_range = (index_range[0], index_range[1])
        valid_index_ranges.append(valid_range)

    im_subset = edax_ds.data[
        slice(valid_index_ranges[0][0], valid_index_ranges[0][1]),
        slice(valid_index_ranges[1][0], valid_index_ranges[1][1]),
        channel_index,
    ].copy()
    del edax_ds
    return im_subset
