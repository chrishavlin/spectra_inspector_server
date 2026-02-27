import numpy as np

from spectra_inspector_server._file_tree_handling import EDAXPathHandler
from spectra_inspector_server.model import EDAX_axis, Spectrum1d


class OperationEDAXStateHandler:
    def __init__(self, ph: EDAXPathHandler) -> None:
        self.ph = ph

    def _validate_index_ranges(
        self, sample_name: str, input_index_ranges: list[tuple[int, int] | None]
    ):

        edax_ds = self.ph.load_edax(sample_name)

        valid_index_ranges: list[tuple[int, int]] = []

        for index_id, index_range in enumerate(input_index_ranges):
            valid_range: tuple[int, int]
            if index_range is None:
                valid_range = (0, edax_ds.axes_by_index[index_id].size)
            else:
                valid_range = (index_range[0], index_range[1])
            valid_index_ranges.append(valid_range)
        return valid_index_ranges

    def get_sample_axes(self, sample_name: str) -> list[EDAX_axis]:
        edax_ds = self.ph.load_edax(sample_name)
        return edax_ds.axes.copy()

    def get_image(
        self,
        sample_name: str,
        channel_index: int | tuple[int, int],
        index0_range: tuple[int, int] | None = None,
        index1_range: tuple[int, int] | None = None,
    ):

        input_index_ranges = [index0_range, index1_range]
        valid_index_ranges = self._validate_index_ranges(
            sample_name, input_index_ranges
        )

        if isinstance(channel_index, tuple):
            channel_slice = slice(channel_index[0], channel_index[1])
        elif isinstance(channel_index, int):
            channel_slice = channel_index
        else:
            msg = f"unexpected type for channel_index: must be int or (int, int), but {channel_index=}"
            raise TypeError(msg)

        edax_ds = self.ph.load_edax(sample_name)
        return edax_ds.data[
            slice(valid_index_ranges[0][0], valid_index_ranges[0][1]),
            slice(valid_index_ranges[1][0], valid_index_ranges[1][1]),
            channel_slice,
        ].copy()

    def get_multi_channel_intensity_image(
        self,
        sample_name: str,
        channel_range: tuple[int, int],
        index0_range: tuple[int, int] | None = None,
        index1_range: tuple[int, int] | None = None,
        chunking_index: int = 0,
        chunksize: int = 32,
    ):

        input_index_ranges = [index0_range, index1_range]
        valid_index_ranges = self._validate_index_ranges(
            sample_name, input_index_ranges
        )
        index_ranges = [valid_index_ranges[0], valid_index_ranges[1], channel_range]

        orig_ranges = index_ranges.copy()

        final_shape: tuple[int, int] = tuple(
            [indx[1] - indx[0] for indx in index_ranges[:-1]]
        )

        index_offsets = [indx[0] for indx in index_ranges[:-1]]
        im_output = np.zeros(final_shape)

        assert im_output.ndim == 2

        i_chunk_0 = orig_ranges[chunking_index][0]
        while i_chunk_0 < orig_ranges[chunking_index][1]:
            i_chunk_1 = i_chunk_0 + chunksize
            i_chunk_1 = min(i_chunk_1, orig_ranges[chunking_index][1])

            index_ranges[chunking_index] = (i_chunk_0, i_chunk_1)

            im = self.get_image(
                sample_name,
                index_ranges[2],
                index0_range=index_ranges[0],
                index1_range=index_ranges[1],
            )

            im_subset = im.sum(axis=-1)

            # find the indices to put it in
            slcs = [
                slice(
                    index_ranges[idim][0] - index_offsets[idim],
                    index_ranges[idim][1] - index_offsets[idim],
                )
                for idim in range(2)
            ]
            im_output[slcs[0], slcs[1]] = im_output[slcs[0], slcs[1]] + im_subset

            i_chunk_0 += chunksize

        return im_output

    def get_spectrum(
        self,
        sample_name: str,
        channel_range: tuple[int, int] | None = None,
        index0_range: tuple[int, int] | None = None,
        index1_range: tuple[int, int] | None = None,
        chunking_index: int = 0,
        chunksize: int = 32,
    ) -> Spectrum1d:

        input_index_ranges = [index0_range, index1_range, channel_range]
        valid_index_ranges = self._validate_index_ranges(
            sample_name, input_index_ranges
        )
        index_ranges = [
            valid_index_ranges[0],
            valid_index_ranges[1],
            valid_index_ranges[2],
        ]

        orig_ranges = index_ranges.copy()

        final_shape = (index_ranges[2][1] - index_ranges[2][0],)

        im_output = np.zeros(final_shape)

        assert im_output.ndim == 1

        i_chunk_0 = orig_ranges[chunking_index][0]
        while i_chunk_0 < orig_ranges[chunking_index][1]:
            i_chunk_1 = i_chunk_0 + chunksize
            i_chunk_1 = min(i_chunk_1, orig_ranges[chunking_index][1])

            index_ranges[chunking_index] = (i_chunk_0, i_chunk_1)

            im = self.get_image(
                sample_name,
                index_ranges[2],
                index0_range=index_ranges[0],
                index1_range=index_ranges[1],
            )

            im_reduced = im.sum(axis=0).sum(axis=0)
            assert im_reduced.size == im_output.size
            im_output = im_output + im_reduced

            i_chunk_0 += chunksize

        energy_channel_axis = np.arange(index_ranges[2][0], index_ranges[2][1])

        return Spectrum1d(energy=energy_channel_axis, intensity=im_output)
